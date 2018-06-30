from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import json
from datetime import datetime, timedelta
import time
import re
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

import calendar
from .models import Question, SmsMessages

false = False

messages = json.loads(file('messages.txt', 'r').read())['messages']

def graph_test(request):
    context = {}
    return render(request, 'polls/graph_test.html', context)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list,
    'message_list': messages}
    return render(request, 'polls/index.html', context)
    
@csrf_exempt
def upload_file(request):
    print 'request = ', request.FILES['input_file']
    myfile = request.FILES['input_file']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    sms_messages = json.loads(file(filename, 'r').read())['messages']
    test_sms_trans(sms_messages)

    print 'uploaded_file_url = ', uploaded_file_url
    print "upload_file called"
    file_contents = request.GET.get('input_file')
    print 'file_contents = ', file_contents
    
    ordered_sms_list = SmsMessages.objects.order_by('sms_received_time')
    context = {}
    context['sms_messages'] = ordered_sms_list
    return render(request, 'polls/sms_report.html', context)
    #return render(request, 'polls/index.html', context)


def test_sms_trans(sms_messages):
    #sms_messages = json.loads(file('messages.txt', 'r').read())['messages']
    transaction_time_not_found = []
    for message in sms_messages:
        sms_text = message['text']
        sms_text = message['text']
        lower_caps_sms_text = sms_text.lower() #sometime you get CREDIT or credit 

        if 'stmt' in lower_caps_sms_text or not ('credit' in lower_caps_sms_text and 'card' in lower_caps_sms_text): #Creditcard or credit card, stmt is statement req
            continue

        print '\n\nmessage = ', message['text']
        sender_id = message['number'].split('-')[1] #VK-HDFCBK - removing VK (unwanted stuff)
        print 'sender_id = ', sender_id
        sms_recieve_time_str = ' '.join(message['datetime'].split()[:-1])
        print 'sms_recieve_time_str = ', sms_recieve_time_str
        sms_recieve_time_obj = datetime.strptime(sms_recieve_time_str, '%Y-%m-%d %H:%M:%S')
        
        '''
        timestamp = message['timestamp']
        sms_recieve_time_str = time.strftime("%a %d %b %Y %H:%M:%S", time.gmtime(timestamp / 1000.0)) #remove GMT and check
        sms_recieve_time_obj = datetime.strptime(sms_recieve_time_str, '%a %d %b %Y %H:%M:%S') + timedelta(hours=5, minutes=30)
        print 'sms_recieve_time_str = ', sms_recieve_time_obj
        '''

        transaction_date = re.search(r'(\d+-\d+-\d+)',sms_text)
        transaction_time = re.search(r'(:\d+:\d+:\d+)',sms_text)
        if transaction_date and transaction_time: #SOME BANKS PROVIDE ONLY TRANSCATION DATE - TRAN TIME NOT PRESENT (HSBC)
            transaction_date_time_str = transaction_date.group() + ' ' + transaction_time.group()[1:]
            transaction_date_time_obj = datetime.strptime(transaction_date_time_str, '%Y-%m-%d %H:%M:%S')
            print 'transaction_date_time_obj = ', transaction_date_time_obj 

        else: 
            transaction_date_time_obj = sms_recieve_time_obj

        
        if 'INR' in sms_text:
            transaction_amount = sms_text.split('INR')[1].strip().split()[0]
        elif 'Rs.' in sms_text:
            transaction_amount = sms_text.split('Rs.')[1].strip().split()[0]

        print 'transaction_amount = ', transaction_amount

        if sender_id == 'HSBCIN':
            credit_card_number_search = re.search(r'(xxxx\d+\d+\d+\d)', lower_caps_sms_text)
            if not credit_card_number_search:
                credit_card_number_search = re.search(r'(ending \d+\d+\d+\d)', lower_caps_sms_text)
                credit_card_number = credit_card_number_search.group().split('ending')[1].strip()
            else: 
                credit_card_number = credit_card_number_search.group().strip('xxxx ')
        elif sender_id == 'HDFCBK':
            credit_card_number_search = re.search(r'(ending \d+\d+\d+\d)', lower_caps_sms_text)
            if not credit_card_number_search:
                credit_card_number_search = re.search(r'(xxxx \d+\d+\d+\d)', lower_caps_sms_text)
                credit_card_number = credit_card_number_search.group().split('xxxx')[1].strip()
            else:
                credit_card_number = credit_card_number_search.group().split('ending')[1].strip()

        SmsMessages.objects.get_or_create(sender_id=sender_id, credit_card_number=credit_card_number, amount=transaction_amount, 
            transaction_date_time=transaction_date_time_obj, sms_received_time=sms_recieve_time_obj)



    print transaction_time_not_found
    print len(transaction_time_not_found)

def display_messages(request):
    ordered_sms_list = SmsMessages.objects.order_by('sms_received_time')
    context = {}
    context['sms_messages'] = ordered_sms_list
    return render(request, 'polls/sms_report.html', context)

def get_all_transaction_month_years():
    all_dates = SmsMessages.objects.order_by('sms_received_time').values_list('sms_received_time', flat=True).distinct()
    trans_month_years = []

    for date in all_dates:
        trans_month_year = str(date.month) + '-' + str(date.year)
        if not trans_month_year in trans_month_years:
            trans_month_years.append(trans_month_year)

    print 'trans_month_years = ', trans_month_years
    return trans_month_years


def monthly_analytics(request):
    context = {}
    monthly_transactions_dict = {} #{'may-2017-hsbc' :[card, total_amount, total_trans]}
    monthly_transactions_dict_list = []
    all_banks = SmsMessages.objects.all().values_list('sender_id', flat=True).distinct()

    trans_month_years = get_all_transaction_month_years()

    for trans_month_year in trans_month_years:
        month = int(trans_month_year.split('-')[0])
        year = int(trans_month_year.split('-')[1])
        all_current_month_year_transactions = SmsMessages.objects.filter(sms_received_time__year=year, sms_received_time__month=month)
        for bank in all_banks:
            current_bank_trans = all_current_month_year_transactions.filter(sender_id=bank)
            total_amount = current_bank_trans.aggregate(Sum('amount'))['amount__sum']
            total_trans = current_bank_trans.count()
            card_number = current_bank_trans[0].credit_card_number
            monthly_transactions_dict[trans_month_year + '-' + bank] = [card_number, total_amount, total_trans]
            new_trans_month_year = calendar.month_name[month] + '-' + str(year)
            current_month_bank_dict = {'month_year':new_trans_month_year, 'bank':bank, 'card_number':card_number, 'total_amount': total_amount, 'total_trans': total_trans}
            monthly_transactions_dict_list.append(current_month_bank_dict)
    

    print 'monthly_transactions_dict_list = ', monthly_transactions_dict_list
    context['monthly_transactions_dict_list'] = monthly_transactions_dict_list
    return render(request, 'polls/monthly_report.html', context)


def new_get_all_transaction_month_years():
    all_dates = SmsMessages.objects.order_by('sms_received_time').values_list('sms_received_time', flat=True).distinct()
    trans_month_years = []

    for date in all_dates:
        trans_month_year = str(calendar.month_name[int(date.month)]) + '-' + str(date.year)
        if not trans_month_year in trans_month_years:
            trans_month_years.append(trans_month_year)

    print 'trans_month_years = ', trans_month_years
    return trans_month_years


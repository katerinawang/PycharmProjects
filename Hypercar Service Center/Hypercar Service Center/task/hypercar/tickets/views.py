from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect

ticket = {'change_oil': [[], 2], 'inflate_tires': [[], 5], 'diagnostic': [[], 30]}
ticket_num = 0
next_num = None

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(f'<h2>Welcome to the Hypercar Service!</h2>')


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'services': ticket.keys()})


class TicketView(View):
    def get(self, request, link, *args, **kwargs):
        global ticket_num
        time_count = 0
        for name, (count, time) in ticket.items():
            time_count += len(count) * time
            print(ticket)
            if name == link:
                break
        ticket_num += 1
        ticket[link][0].append(ticket_num)
        return render(request, 'tickets/get_ticket.html', context={'number': ticket_num, 'wait': time_count})


class OperatorView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/processing.html', context={'queue': [len(item[0]) for item in ticket.values()]})

    def post(self, request, *args, **kwargs):
        global next_num
        for number in [item[0] for item in ticket.values()]:
            if len(number) != 0:
                next_num = number.pop(0)
                break
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', context={'next': next_num})

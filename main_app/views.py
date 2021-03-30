from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
# bring in some things to make auth easier
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# bring in decorator
from django.contrib.auth.decorators import login_required


# attempt form
from django.forms.models import model_to_dict

# import models
from .models import Machine
# access the FeedingForm
from .forms import MaintenanceForm, MachineForm

# import Django form classes
# these handle CRUD for us
# we will comment this one out
class MachineCreate(CreateView):
    model = Machine
    # fields = '__all__'s
    success_url = '/machines'

# changed to use custom cat_update function with decorator
class MachineUpdate(UpdateView):
    model = Machine
    fields = ['name', 'operator', 'manufacturedYear', 'partNumber']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/machines/' + str(self.object.pk))


class MachineDelete(DeleteView):
    model = Machine
    success_url = '/machines'


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# Machines
@login_required()
def machines_index(request):
    # we have access to the user request.user
    machines = Machine.objects.filter(user= request.user)
    return render(request, 'machines/index.html', { 'machines': machines })

@login_required()
def machines_show(request, machine_id):
    # we get access to that machine_id variable
    # query for the specific machine clicked
    machine = Machine.objects.get(id=machine_id)
    # lets make a feeding_form
    maintenance_form = MaintenanceForm()
    return render(request, 'machines/show.html', { 
        'machine': machine,
        'maintenance_form': maintenance_form 
    })

#refactor to custom update to use @login_required decorator
@login_required
def machines_update(request, pk):
    if request.POST:
        print('its an update request')
        our_machine = Machine.objects.get(id=pk)
        our_machine.name = request.POST.get('name')
        our_machine.operator = request.POST.get('operator')
        our_machine.manufacturedYear = request.POST.get('manufacturedYear')
        our_machine.partNumber = request.POST.get('partNumber')
        our_machine.save()
        return redirect('machines')
    machine = Machine.objects.get(id=pk)
    machineform = MachineForm(initial=model_to_dict(machine)) 
    return render(request, 'machines/machine_form.html', { 'form': machineform })

# build out cats_new custom to use the userId
@login_required()
def machines_new(request):
    machine_form = MachineForm(request.POST or None)
    # if the form was posted and valid
    if request.POST and machine_form.is_valid():
        new_machine = machine_form.save(commit=False)
        new_machine.user = request.user
        new_machine.save()
        # redirect to index
        return redirect('index')
    else:
        return render(request, 'machines/new.html', { 'machine_form': machine_form })

# Maintenance
@login_required()
def add_maintenance(request, pk):
    form = MaintenanceForm(request.POST)
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.machine_id = pk
        new_maintenance.save()
    return redirect('machines_show', machine_id = pk)

def sign_up(request):
    error_message= ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ok user created log them in
            login(request, user)
            return redirect('index')
        else:
            error_message='That was a no go. Invalid signup'
        # this will run after if it's not a POST or it was invalid
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
            'form': form,
            'error_message': error_message
        })


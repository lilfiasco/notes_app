from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView, 
    View, 
    DetailView,
    UpdateView
)

from .models import ToDoNote
from .forms import NoteForm


# def get_base(request) -> HttpResponse:
#     return render (request, 'base.html')

def get_base(request) -> HttpResponse:
    form = AuthenticationForm
    return render (request, 'base.html', context={ 'form': form })

class CreateNoteView(CreateView):
    """
    Add new Note.
    """

    form_class = NoteForm
    success_url = reverse_lazy('create_note')
    template_name = 'notes/add_note.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.user
        print('FFFFFFFFF: ', context)
        return context

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        print("AZAZAZA: ", form.errors)
        return super().form_invalid(form)

    def form_valid(self, form): 
        try:
            form.instance.author = self.request.user
            note = form.save(commit=False)
            note.save()
            print("sssssssssssss" ,note)
            return render(self.request, 'notes/add_note_success.html')
        except ValueError as e:
            form.add_error('image', str(e))  
            return self.form_invalid(form)


class UserNotesListView(ListView):
    """
    NoteListView for User.
    """

    model = ToDoNote
    template_name = 'notes/user_notes.html'
    context_object_name = 'todo_notes'

    def get_queryset(self):
        return ToDoNote.objects.filter(author=self.request.user)


class NoteEditView(UpdateView):
    """
    NoteEditView.
    Note removal too.
    """

    model = ToDoNote
    template_name = 'notes/note_edit.html'
    fields = ['title', 'description', 'status']
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    
    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            obj = self.get_object()
            obj.delete()
            return HttpResponseRedirect(reverse_lazy('user_note'))
        return super().post(request, *args, **kwargs)
        


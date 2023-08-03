from django.urls import path
from .views import(
    get_base,
    CreateNoteView,
    UserNotesListView,
    NoteEditView,
    )


urlpatterns = [
    path('', get_base),
    path('notes/', UserNotesListView.as_view(), name='user_note'),
    path('notes/create', UserNotesListView.as_view(), name='user_note'),
    path('notes/update/<int:pk>/', NoteEditView.as_view(), name='update_note'),
    
]
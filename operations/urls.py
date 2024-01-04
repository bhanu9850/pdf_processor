from . import views
from django.urls import path 

urlpatterns=[
    path('', views.home, name='home'),
    path('merge_pdf/', views.merge_pdf, name='merge_pdf'),
    path('compress_pdf/', views.compress_pdf, name='compress_pdf'),
    path('encrypt/', views.encrypt, name='encrypt'),
    path('decrypt/', views.decrypt, name='decrypt'),
    path('pdf_to_word/', views.pdf_to_word, name='pdf_to_word'),
    path('word_to_pdf/', views.word_to_pdf, name='word_to_pdf'),
    
]
from django.shortcuts import render
import PyPDF2
import time
import io
from django.http import HttpResponse
from PyPDF2 import PdfReader,PdfWriter
import os
from django.core.files.storage import FileSystemStorage
from docx2pdf import convert
from pdf2docx import Converter


def home(request):
    return render(request,'homepage.html')

def merge_pdf(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pdf_files')
        merger = PyPDF2.PdfMerger()
        for file in files:
            merger.append(file)
        merged_file_path = 'merged_file.pdf'
        with open(merged_file_path, 'wb') as merged_file:
            merger.write(merged_file)
        time.sleep(5)
        # Serve the merged PDF for download
        with open(merged_file_path, 'rb') as merged_file:
            response = HttpResponse(merged_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=merged_file.pdf'
            return response
    else:
        return render(request,'merge_pdf.html')        
    
    return render(request, 'merge_pdf.html')

def compress_pdf(request):
    if request.method == 'POST':
        files = request.FILES.getlist('pdf_file')
        
        # Ensure at least one file is uploaded
        if files:
            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfWriter()
            
            # Iterate through each uploaded PDF file
            for file in files:
                # Create a PdfReader object from the uploaded file
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Iterate through each page and add it to the PDF writer object
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)
            
            # Create a byte stream to write the compressed PDF
            compressed_pdf_bytes = io.BytesIO()
            
            # Write the compressed PDF to the byte stream
            pdf_writer.write(compressed_pdf_bytes)
            
            compressed_pdf_file_path = 'compressed_pdf.pdf'
            with open(compressed_pdf_file_path, 'wb') as compressed_pdf_file:
                compressed_pdf_file.write(compressed_pdf_bytes.getvalue())
            
            with open(compressed_pdf_file_path, 'rb') as compressed_pdf_file:
                response = HttpResponse(compressed_pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=compressed_pdf.pdf'
                return response
        else:
            # Handle case when no file is uploaded
            return render(request, 'compress_pdf.html', {'error_message': 'Please upload a PDF file.'})
    
    return render(request, 'compress_pdf.html') 

def encrypt(request):
    if request.method == "POST":
        # Get the uploaded PDF file from the form
        file = request.FILES.get('pdf_file')
        
        # Check if a file is uploaded
        if not file:
            return render(request, 'encryption.html', {'error_message': 'Please upload a PDF file.'})
        
        # Read the PDF file using PyPDF2
        reader = PdfReader(file)
        writer = PdfWriter()
        
        # Add each page from the reader to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Get the password from the form input
        password = request.POST.get('password', '')
        
        # Check if password is provided
        if not password:
            return render(request, 'encryption.html', {'error_message': 'Please enter a password.'})
        
        # Encrypt the PDF with the provided password
        writer.encrypt(password)

        # Save the encrypted PDF to a file
        encrypted_pdf_path = "encrypted-pdf.pdf"
        with open(encrypted_pdf_path, "wb") as f:
            writer.write(f)

        # Serve the encrypted PDF as a download response
        with open(encrypted_pdf_path, 'rb') as encrypted_pdf_file:
            response = HttpResponse(encrypted_pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=encrypted-pdf.pdf'
            return response
    else:
        # If the request method is not POST, render the encryption.html template
        return render(request, 'encryption.html')


def decrypt(request):
    if request.method == 'POST':
        file = request.FILES.get('pdf_file')
        if not file:
            return render(request,decrypt.html,"{'error_message':please upload a file}")

        reader = PdfReader(file)
        writer = PdfWriter()
        password = request.POST.get('password','')
        if not password:
            return render(request, 'encryption.html', {'error_message': 'Please enter a password.'})
        if reader.is_encrypted:
            reader.decrypt(password)    
        for page in reader.pages:
            writer.add_page(page)  
        decrypted_pdf_path = "decrypted-pdf.pdf"
        with open(decrypted_pdf_path, "wb") as f:
            writer.write(f)

        
        with open(decrypted_pdf_path, 'rb') as decrypted_pdf_file:
            response = HttpResponse(decrypted_pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=decrypted-pdf.pdf'
            return response      
    else:
       return render(request, 'decryption.html')

def word_to_pdf(request):
    if request.method == 'POST' and request.FILES['docx_file']:
        # Handle uploaded file
        uploaded_file = request.FILES['docx_file']
        
        # Save the uploaded file temporarily
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_path = fs.path(filename)
        
        # Convert the file
        pdf_filename = filename.replace('.docx', '.pdf')
        output_pdf_path = fs.path(pdf_filename)
        convert(uploaded_file_path, output_pdf_path)
        
        # Provide the PDF file for download
        with open(output_pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            return response
    
    return render(request, 'word_to_pdf.html')   

def pdf_to_word(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        # Handle uploaded file
        try:
            uploaded_file = request.FILES['pdf_file']
            
            # Save the uploaded file temporarily
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = fs.path(filename)
            
            # Convert the file
            docx_filename = filename.replace('.pdf', '.docx')
            output_docx_path = fs.path(docx_filename)
            
            # Use pdf2docx library to convert PDF to DOCX
            converter = Converter(uploaded_file_path)
            converter.convert(output_docx_path)
            converter.close()
            
            # Provide the DOCX file for download
            with open(output_docx_path, 'rb') as docx_file:
                response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = f'attachment; filename="{docx_filename}"'
                return response
        except:
            error_message = "Error converting the PDF. Please ensure the PDF is not encrypted or corrupted."
            return HttpResponse (error_message)       
    
    return render(request, 'pdf_to_word.html')
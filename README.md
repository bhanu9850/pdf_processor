PDF Processor Application
Overview
The PDF Processor Application, built using Django and Python, provides a comprehensive set of functionalities for handling PDF documents. This application facilitates various operations such as merging, compressing, converting Word to PDF and vice versa, as well as encryption and decryption of PDF files.

Features
PDF Upload: Upload PDF documents to the application.
Merging: Combine multiple PDF files into a single document.
Compression: Reduce the file size of PDF documents.
Word to PDF Conversion: Convert Word documents to PDF format.
PDF to Word Conversion: Convert PDF documents to Word format.
Encryption: Secure PDF files with encryption.
Decryption: Decrypt encrypted PDF files.

Requirements
Python (version 3.8)
Django (version 3.0.5)
PyPDF library


Clone the repository:
git clone https://github.com//pdf-processor.git

Navigate to the project directory:
cd pdf-processor

Install the required packages:

Run migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

Acknowledgements
Django Documentation
Python Documentation
PyPDF2
python-docx

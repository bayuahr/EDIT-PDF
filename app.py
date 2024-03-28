from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import streamlit as st
import base64
def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display =  f"""<embed
    class="pdfobject"
    type="application/pdf"
    title="Embedded PDF"
    src="data:application/pdf;base64,{base64_pdf}"
    style="overflow: auto; width: 500px; height: 800px;">"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
def main():
    c1,c2=st.columns(2)
    
    with c1:
        st.title("PDF Editor")
        # Input fields
        nomor_spak = st.text_input("Nomor SPAK")
        nama_tertanggung = st.text_input("Nama Tertanggung")
        cabang_so = st.text_input("Cabang Sales Office")
        description = st.text_area("Description")
        nama_pemegang_polis = st.text_input("Nama Pemegang Polis")
        nama_calon_tertanggung = st.text_input("Nama Calon Tertanggung")
        nama_agen = st.text_input("Nama Agen")

        # Edit PDF when button is clicked
    if st.button("Process PDF"):
        # Provide a download link for the edited PDF file
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColorRGB(0, 0, 0)
        can.setFont("Times-Roman", 12)
        # NOMOR SPAJ
        can.drawString(234, 645, nomor_spak)
        # Nama Calon Tertanggung
        can.drawString(239, 630, nama_tertanggung)
        # Cabang
        can.drawString(250, 615, cabang_so)
        # Calon Pemegang Polis
        can.drawString(40, 100, nama_pemegang_polis)
        # Calon Tertanggung
        can.drawString(250, 100, nama_calon_tertanggung)
        # Agen
        can.drawString(415, 100, nama_agen)

        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open("axa.pdf", "rb"))
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        outputStream = open("dest.pdf", "wb")
        output.write(outputStream)
        outputStream.close()
        with c2:
            displayPDF("dest.pdf")
        st.success("PDF processed successfully!")
if __name__ == "__main__":
    main()

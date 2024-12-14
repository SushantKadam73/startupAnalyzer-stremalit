import markdown2
import pdfkit
company_name="100xengineers"
def md_to_pdf(company_name,given_filename):
    filename = "knowlege_base/"+company_name+"/"+given_filename
    mode = "r"
    from markdown_pdf import MarkdownPdf, Section
    with open(filename, mode) as file:
        markdown_text = file.read()
    pdf = MarkdownPdf()
    pdf.meta["title"] = 'output'
    pdf.add_section(Section(markdown_text, toc=False))
    pdf.save('output.pdf')
    html_text = markdown2.markdown(markdown_text)
    pdfkit.from_string(html_text, "output.pdf")
md_to_pdf("100xengineers","product evalution engine_report.md")
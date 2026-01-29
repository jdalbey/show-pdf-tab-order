# show-pdf-tab-order
A simple command line utility to display the tab order of fields in a PDF.
### Features
* Accepts the name of a PDF file on the command line
* Analyzes the PDF content and determines the tab order of fillable fields in the document.
* Displays a list of fields in tab order, using the top-down,left-right pattern used by Evince and Firefox.
* Multi-column output includes coordinates of fields.

### Motivation
I created a fillable PDF using Libre Office Draw. I carefully completed the tab order property to sequence the fields as I desired. But when viewed in Evince or Firefox it ignored my specified tab order. After wasting most of a day with a stupid chatbot that told me how the internal structure of my PDF was messed up, I finally discovered the real issue: Evince and Firefox *ignore* the internal field order given in the PDF.  They use their own algorithm to provide what is the most common sense result: tab from top-down, left-right. 

**HOWEVER**, even minisucle differences in field position can affect tab order.  E.g., in my document one field was positioned .01cm different than another field which resulted in it being included in the tab order on the previous row. Relying on human eyesight to determine field alignment was unreliable.

So I had Claude code up a quick script to display the fields in tab order using top-down, left-right and their coordinates so I can verify the layout. This tool instantly revealed where my fields were out of position and I was quickly able to correct it in Libre Office Draw. 

## Usage

Download the python script and run from the command line.  
Syntax:   
`python show_tab_order.py FILENAME`

Sample output:
```
Analyzing: demo_form.pdf
======================================================================

Evince tab order (top to bottom, left to right):

#    Field Name             Center X   Center Y Rect (x1, y1, x2, y2)
----------------------------------------------------------------------------------------------------
1    LastName                 135.01     511.78 (54.00, 501.56, 216.03, 522.00)
2    Firstname                301.79     511.78 (252.28, 501.56, 351.30, 522.00)
3    Date                     594.16     511.78 (558.14, 501.56, 630.17, 522.00)
4    Phone                    463.34     511.64 (402.24, 501.42, 524.44, 521.86)
5    Brand                     68.19     436.80 (34.02, 424.32, 102.36, 449.29)
6    ProductCode              134.94     436.80 (106.58, 424.32, 163.31, 449.29)
7    Description              263.81     436.80 (166.96, 424.32, 360.65, 449.29)
```

## Dependencies
Requires: [qpdf](https://github.com/qpdf/qpdf)  
Install using: `sudo apt-get install qpdf`

## License
MIT License



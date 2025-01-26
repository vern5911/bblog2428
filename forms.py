from flask_wtf import Form
from wtforms import IntegerField, StringField, TextAreaField, validators
from wtforms.validators import DataRequired

# Create Class for validation of Bibleblog DB Table records
class BblogForm(Form):
    bid = IntegerField('Bid')
    bdate = StringField('Bdate', [validators.Length(min=10,max=10)])
    doy = IntegerField('Doy')
    book = StringField('Book')
    chapter = IntegerField('Chapter')
    feedback = TextAreaField('Feedback', [validators.DataRequired()])

# Create a Books of the Bible dictionary.
books_dict={}
Books={'Gn':'Genesis','Ex':'Exodus','Lv':'Leviticus','Nm':'Numbers',
        'Dt':'Dueternomy','Jos':'Joshua','Jgs':'Judges','Ru':'Ruth',
        '1Sm':'1 Samuel','2Sm':'2 Samuel','1Kgs':'1 Kings',
        '2Kgs':'2 Kings','1Chr':'1 Chronicle','2Chr':'2 Chronicles',
        'Ezr':'Exra','Neh':'Nehemia','Tob':'Tobit','Jdt':'Judith',
        'Est':'Esther','1Mc':'1 Macabees','2Mc':'2 Macabees',
        'Jb':'Job','Ps':'Psalm','Prv':'Proverbs','Eccl':'Ecclesiastes',
        'Sg':'Song of Songs','Wis':'Wisdom','Sir':'','Is':'Isaiah',
        'Jer':'Jeremiah','Lam':'Lamentations','Bar':'Baruk','Ez':'Ezekiel',
        'Dn':'Daniel','Hos':'Hosea','Jl':'Joel','Am':'Amos','Ob':'Obadiah',
        'Jon':'Jonah','Mi':'Micah','Na':'Nahum','Hb':'Habakkuk','Zep':'Zephaniah',
        'Hg':'Haggai','Zec':'Zechariah','Mal':'Malachi','Mt':'Matthew','Mk':'Mark',
        'Lk':'Luke','Jn':'John','Acts':'Acts','Rom':'Romans','1Cor':'1 Corintians',
        '2Cor':'2 Corintians','Gal':'Galatians','Eph':'Ephesians','Phil':'Philippians',
        'Col':'Colossians','1Thes':'1 Thessalonians','2Thes':'2 Thessalonians',
        '1Tim':'1 Timothy','2Tim':'2 Timothy','Ti':'Titus','Phlm':'Philemon',
        'Heb':'Hebrews','Jas':'James','1Pt':'1 Peter','2Pt':'2 Peter','1Jn':'1 John',
        '2Jn':'2 John','3Jn':'3 John','Jude':'Jude','Rv':'Revelations'
        }
books_dict.update(Books)

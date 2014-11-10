Summarizer
==========

Returns top-[n] most relevant sentences from a document.


Installation

    mkvirtualenv --no-site-packages keyptenv # or your preferred method
    git clone https://github.com/lekhakpadmanabh/Summarizer.git
    cd Summarizer
    pip install -r requirements.txt
    python setup.py install --record installed_files.txt

##Usage

    import keyptsummarizer as smrzr
    url = "http://swaminomics.org/can-congress-bounce-back-from-no-3/"

    article = smrzr.Summarizer(url, fmt='md')

You can also specify the number of sentences (defaults to 4) or leave out the `fmt` parameter to get the summary as a list. By default it resorts to using the Goose library, a custom extractor can be specified if it doesn't fit the purpose.

    >>> print article.text # the raw text returned by the extractor
    >>> print article.meta # meta description from webpage, very useful if it exists
    ''
    >>> print article.summary 
    u'Having been thrashed in the general election, and again in the state elections last week in Maharashtra and Haryana, can the Congress bounce back?'
    >>> print article.keypoints
    u'>* In the past, the Congress has often been written off after massive defeats but bounced back.\n>* Wherever the Congress has slipped to third or fourth position in a state, anti-incumbency has favoured the No 2 party, leaving the No 3 party out in the cold.\n>* Despite these setbacks, the Congress remained either No 1 or No 2 in other states.\n>* Even if it slips to No 3 in state after state, it is easily No 2 at the national level.\n'

For no formatting, just use `article = k.Summarizer(url)`

    >>> print article.keypoints
    [u'In the past, the Congress has often been written off after massive defeats but bounced back.',
     u'Wherever the Congress has slipped to third or fourth position in a state, anti-incumbency has favoured the No 2 party, leaving the No 3 party out in the cold.',
     u'Despite these setbacks, the Congress remained either No 1 or No 2 in other states.',
     u'Even if it slips to No 3 in state after state, it is easily No 2 at the national level.']

There is an experimental `entities` attribute for Summarizer instance which prints out any proper nouns it could detect using nltk helpers. Switch it on by using `entities=True` while instantiating Summarizer.

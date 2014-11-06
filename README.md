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

    #summarize directly from link
    url = "http://www.huffingtonpost.com/2014/11/02/pakistan-bomb_n_6089632.html"
    human_summary, key_points = smrzr.summarize_url(url, fmt="md")
    print human_summary
    print key_points


Summarizer
==========

Returns top-[n] most relevant sentences from a document.


##Installation

```bash
mkvirtualenv --no-site-packages keyptenv # or your preferred method
git clone https://github.com/lekhakpadmanabh/Summarizer.git
cd Summarizer
pip install -r requirements.txt
python setup.py install --record installed_files.txt
```

##Usage

```python
import smrzr
url = "http://swaminomics.org/can-congress-bounce-back-from-no-3/"
```

The easiest way to use it is to create an instance of the summarizer class

```python
article = smrzr.Summarizer(url)
```

You can also specify the number of sentences using the optional `num_sentences` (defaults to 4) or specify a `fmt` (defaults to  `'default'`). The default extractor is [goose](https://github.com/grangier/python-goose) which works pretty well for most websites. You can also specify a custom extractor.

The article object has been populated with some attributes,

```python
>>> print article.text # the raw text returned by the extractor
u'Having been thrashed in the general election, and again in the state elections last week in Maharashtra and Haryana, can the Congress bounce back? And if so, how and why?\n\nIn the past, the Congress has often been written off after massive defeats but bounced back. However, we may have entered a new phase. The Congress was able to recover from terrible debacles in the past as long as it remained the second largest party, in state as well as national elections. The reason was simple. Incumbents tend to lose, especially after more than one term, in all democracies. So, even if a Congress state government had performed dreadfully and been ousted by voters, it could hope that the new government would also face anti-incumbency after a few years, and be voted out. In this game, the Congress didn\u2019t have to do anything spectacular while in Opposition. It could just bide its time, and wait for its opponent to make mistakes and be hit by anti-incumbency .\n\nBut that strategy will no longer work in several states. Wherever the Congress has slipped to third or fourth position in a state, anti-incumbency has favoured the No 2 party, leaving the No 3 party out in the cold. The Congress has never been able to bounce back in any state where it has fallen to third position.\n\nThis first happened in Tamil Nadu. The Congress ruled the state till 1967, but lost to the DMK. Congressmen waited confidently for a comeback. But then MG Ramachandran split from the DMK to form the AIADMK. These two parties have occupied the No 1 and 2 positions ever since. The Congress, at No 3, has grown ever weaker.\n\nThe pattern was repeated next in Bihar and Uttar Pradesh. The Congress was thrashed by Lalu Yadav in Bihar in 1990, but was still No 2. Then it slipped to third position in 1995, being overtaken by the BJP as well as Lalu. And later Congress slipped to No 4 after Nitish Kumar split away from Lalu to form the Samta Party, later called the JDU. Even when the Congress returned to power in New Delhi in 2004-14, it remained a pygmy in Bihar.\n\nIn Uttar Pradesh, the largest state, Mulayam Singh Yadav edged out the Congress in the 1989 state election. After that the BJP and BSP came up strongly, relegating Congress to third or fourth position. It was never able to bounce back.\n\nDespite these setbacks, the Congress remained either No 1 or No 2 in other states. This enabled it come back after every defeat, though often as head of a coalition, not in its own right.\n\nBut in the last few years the party has slipped to No 3 or lower in several other states. The top two positions are now occupied in West Bengal by the Trinamool Cogress and Left Front; in Andhra Pradesh by the TDP and YSR Congress; in Haryana by the BJP and INLD; and in Maharashtra by the BJP and Shiv Sena.\n\nToday, the once-mighty Congress rules in only three major states -Karnataka, Kerala and Assam -and some mini-states like Uttarakhand, Himachal Pradesh and Manipur. These states account for less than 80 of the 543 seats in Parliament.\n\nClearly, the Congress can no longer bank on anti-incumbency to return to power in places where it has become No 3. It needs a new purpose, a new message to enthuse voters. Alas, its leadership shows no sign of acknowledging this. Some Congressmen have the forlorn hope that Priyanka Gandhi can be a new savior. But the dubious deals of her husband were a key reason for the party\u2019s decimation in Haryana, so she could be more a liability than an asset.\n\nSome intellectuals have suggested that the Congress should sack the Gandhi family, or at least Rahul Gandhi. Sorry, but the party is a bunch of opportunists held together only by the Gandhi family. Without the family, it will split into irrelevancy.\n\nAnd the party retains one trump card. Even if it slips to No 3 in state after state, it is easily No 2 at the national level. Regional parties may hammer it in state elections, but no single regional party can beat it at the national level. So, when anti-incumbency duly hits the BJP after one, two or even three terms, the Congress can still hope to replace it at the head of a diverse coalition. Coalition dharma may mean the Congress will have to swallow even more humiliations than were heaped on it by the Left Front in 2004 and by Mamata Banerjee in 2009. But all is not lost.'
```

The meta description from the webpage, very useful if it exists and is given high preference as the single-line summary candidate

```python
>>> print article.meta
''
```

In this case there was none but don't worry `smrzr` has it covered

```python
>>> print article.summary 
u'Having been thrashed in the general election, and again in the state elections last week in Maharashtra and Haryana, can the Congress bounce back?'
```

Get the key points

```python
>>> print article.keypoints
[u'In the past, the Congress has often been written off after massive defeats but bounced back.',
 u'Wherever the Congress has slipped to third or fourth position in a state, anti-incumbency has favoured the No 2 party, leaving the No 3 party out in the cold.',
 u'Despite these setbacks, the Congress remained either No 1 or No 2 in other states.',
 u'Even if it slips to No 3 in state after state, it is easily No 2 at the national level.']
```
There is also a command line interface, usage examples:

```bash
smrzr --url <url here> --lines=3
smrzr -u <url here> -l=3 #non-verbose
smrzr --text <text here>
smrzr --file <filename>
```

You'd need to make it executable (or alias it), otherwise use `python -m smrzr [args]`

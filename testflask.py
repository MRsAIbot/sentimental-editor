import requests

articleContent = 'I wonder what the wired community thinks of the Queen of England going on online and possibly having her own encoded email address for friends and family beyond the reach of hackers? Let me hasten to add that I am not suggesting that this is the case, but just fishing for ideas from others more computer literate than I ! How feasible is this? Back in the 1950s she was modern enough to insist on her coronation being televised when advised against it by the British establishment including Winston Churchill who warned her not to let intrustive cameras in her life - I have just published a Kindle/Amazon book about this entitled The Queen of England and the Unknown Schoolboy when Buckingham Palace had its own post office and got its stamps free of charge! - and back then the fifties were of course the decade of television. So maybe she is abreast of the times yet again with computers and emails? She has her own website managed for her at the palace and to save money on stamps she may well be a keen emailer! Bur how would her emails be protected? Would this be a risk too far? '
articleTitle = 'Queen goes wired'

payload = {'article': articleContent, 'title': articleTitle}
r = requests.post("http://condenast.ngrok.com/sentimental/", data=payload)

print r.text
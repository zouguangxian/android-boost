import os,sys,re,getopt
import json, httplib

PROJECTS = [
'https://github.com/TheRealKerni/HockeyKit',
'https://github.com/Redth/PushSharp',
'https://github.com/chrisbanes/Android-PullToRefresh',
'https://github.com/harism/android_page_curl',
'https://github.com/sparcedge/knappsack',
'https://github.com/mttkay/ignition',
'https://github.com/mttkay/droid-fu',
'https://github.com/ACRA/acra',
'https://github.com/excilys/androidannotations',
'https://github.com/jfeinstein10/SlidingMenu',
'https://github.com/johnkil/Android-AppMsg',
'https://github.com/bauerca/drag-sort-listview',
'https://github.com/openaphid/android-flip',
'https://github.com/JakeWharton/ActionBarSherlock',
'https://github.com/JakeWharton/Android-ViewPagerIndicator',
'https://github.com/JakeWharton/NineOldAndroids',
'https://github.com/alexgorbatchev/SyntaxHighlighter',
'https://github.com/roboguice/roboguice',
'https://github.com/github/android',
'https://github.com/cyrilmottier/GreenDroid',
'https://github.com/johannilsson/android-actionbar',
'https://github.com/jgilfelt/android-mapviewballoons',
'https://github.com/octo-online/robospice',
'https://github.com/novoda/RESTProvider',
'https://github.com/loopj/android-async-http',
'https://github.com/greenrobot/greenDAO',
'https://github.com/greenrobot/EventBus',
'https://github.com/square/tape',
'https://github.com/androidquery/androidquery',
'https://github.com/jgilfelt/android-adt-templates',
'https://github.com/cyrilmottier/Polaris',
'https://github.com/keyboardsurfer/Crouton',
'https://github.com/alljoyn/alljoyn_core',
'https://github.com/robotmedia/AndroidBillingLibrary',
'https://github.com/mitmel/Android-Image-Cache',
'https://github.com/jgilfelt/android-mapviewballoons',
'https://github.com/jblough/Android-Pdf-Viewer-Library',
'https://github.com/ahorn/android-rss',
'https://github.com/dmitry-zaitsev/AndroidSideMenu',
'https://github.com/Flowdalic/asmack',
'https://github.com/novoda/RESTProvider',
'https://github.com/siyamed/android-satellite-menu',
'https://github.com/47deg/android-swipelistview',
'https://github.com/pakerfeldt/android-viewflow',
'https://github.com/guardianproject/onionkit',
'https://github.com/encog/encog-java-core',
'https://github.com/andresy/torch',
'https://github.com/foxykeep/datadroid',
]

def usage():
	print "%s -t TOKEN" % (sys.argv[0])

def main(argv):
	try:
        	opts, args = getopt.getopt(argv[1:], "t:", ["token="])
    	except getopt.GetoptError:
        	usage()
        	sys.exit(2)
	token = ''
	for o, a in opts:
        	if o == "-t":
            		token = a 

	connection = httplib.HTTPSConnection("api.github.com", 443)
	connection.connect()
	dataset = []

	for x in PROJECTS:
		m = re.match('^.*//github.com/(?P<repo>.*)$', x)
		repo = m.group('repo')
		connection.request('GET', '/repos/%s' % (repo), None, {"Authorization": "token %s" % (token)})
		response = connection.getresponse()
		rv = json.loads(response.read())
		if response.status != 200:
			sys.stdout.write("url: %s\nstatus code: %s\nrv: %s\n"%(x, response.status, rv))
			continue
		
		name = rv['name']
		html_url = rv['html_url']
		description = rv['description']
		pushed_at = rv['pushed_at']
		watchers_count = rv['watchers_count']
		forks = rv['forks']
		open_issues_count = rv['open_issues_count']
		dataset.append({ 'name' : name,
			'html_url' : html_url,
			'description' : description,
			'pushed_at' : pushed_at,
			'watchers_count' : watchers_count,
			'forks' : forks,
			'open_issues_count' : open_issues_count
		})
		
	repos = sorted(dataset, key=lambda x: x['forks'], reverse=True)
	for x in repos:
		try:
			print '* [%s](%s)' % (x['name'], x['html_url']) 
			print
			print '    stared:`%s`, forks:`%s`, issues:`%s`' % (x['watchers_count'], x['forks'], x['open_issues_count'])
			print
			print '    %s' % (x['description'])
			print
		except:
			#sys.stderr.write("%s\n", x)
			pass
		
if __name__ == '__main__':
	main(sys.argv)
import os, sys, re, getopt
import json, httplib, urllib, urlparse 
import cgi
import pprint

PROJECTS = [
'https://github.com/47deg/android-swipelistview',
'https://github.com/ACRA/acra',
'https://github.com/Flowdalic/asmack',
'https://github.com/Instagram/node2dm',
'https://github.com/JakeWharton/ActionBarSherlock',
'https://github.com/JakeWharton/Android-ViewPagerIndicator',
'https://github.com/JakeWharton/DiskLruCache',
'https://github.com/JakeWharton/NineOldAndroids',
'https://github.com/MasteringOpenCV/code',
'https://github.com/ReadyTalk/avian',
'https://github.com/Redth/PushSharp',
'https://github.com/SimonVT/android-menudrawer',
'https://github.com/TheRealKerni/HockeyKit',
'https://github.com/Themaister/RetroArch',
'https://github.com/Uncodin/bypass',
'https://github.com/WhisperSystems/TextSecure',
'https://github.com/ahorn/android-rss',
'https://github.com/alexgorbatchev/SyntaxHighlighter',
'https://github.com/alljoyn/alljoyn_core',
'https://github.com/andresy/torch',
'https://github.com/androidquery/androidquery',
'https://github.com/appcelerator/titanium_mobile',
'https://github.com/bartaz/impress.js',
'https://github.com/bauerca/drag-sort-listview',
'https://github.com/blueimp/jQuery-File-Upload',
'https://github.com/cgeo/c-geo-opensource',
'https://github.com/chrisbanes/Android-PullToRefresh',
'https://github.com/chrislacy/TweetLanes',
'https://github.com/cobub/razor',
'https://github.com/cocos2d/CocosBuilder',
'https://github.com/cyrilmottier/GreenDroid',
'https://github.com/cyrilmottier/Polaris',
'https://github.com/daCapricorn/ArcMenu',
'https://github.com/daizhenjun/ImageFilterForAndroid',
'https://github.com/dmitry-zaitsev/AndroidSideMenu',
'https://github.com/encog/encog-java-core',
'https://github.com/excilys/androidannotations',
'https://github.com/foxykeep/datadroid',
'https://github.com/github/android',
'https://github.com/github/gauges-android',
'https://github.com/greenrobot/EventBus',
'https://github.com/greenrobot/greenDAO',
'https://github.com/guardianproject/onionkit',
'https://github.com/harism/android_page_curl',
'https://github.com/hrydgard/ppsspp',
'https://github.com/jblough/Android-Pdf-Viewer-Library',
'https://github.com/jfeinstein10/SlidingMenu',
'https://github.com/jgilfelt/android-adt-templates',
'https://github.com/jgilfelt/android-mapviewballoons',
'https://github.com/johannilsson/android-actionbar',
'https://github.com/johndyer/mediaelement',
'https://github.com/johnkil/Android-AppMsg',
'https://github.com/keyboardsurfer/Crouton',
'https://github.com/koush/Superuser',
'https://github.com/loopj/android-async-http',
'https://github.com/madeye/proxydroid',
'https://github.com/maurycyw/StaggeredGridView',
'https://github.com/mitmel/Android-Image-Cache',
'https://github.com/mono/MonoGame',
'https://github.com/mttkay/droid-fu',
'https://github.com/mttkay/ignition',
'https://github.com/nicolas-raoul/Anki-Android',
'https://github.com/nostra13/Android-Universal-Image-Loader',
'https://github.com/novoda/RESTProvider',
'https://github.com/octo-online/robospice',
'https://github.com/openaphid/android-flip',
'https://github.com/pakerfeldt/android-viewflow',
'https://github.com/roboguice/roboguice',
'https://github.com/robotmedia/AndroidBillingLibrary',
'https://github.com/siyamed/android-satellite-menu',
'https://github.com/sparcedge/knappsack',
'https://github.com/square/otto',
'https://github.com/square/tape',
'https://github.com/tjerkw/Android-SlideExpandableListView',
'https://github.com/trentbrooks/AntiMap',
'https://github.com/yixia/FFmpeg-Android',
'https://github.com/yixia/VitamioBundle',
'https://github.com/zouguangxian/andmake',
'https://github.com/zynga/viewporter',
]

LICENSES = {
	'APACHE': 'Apache License',
	'BSD': 'BSD license',
	'GPL-2.0': 'The GNU General Public License.*?1991',
	'GPL-3.0': 'GNU GENERAL PUBLIC LICENSE.*?2007',
	'LGPL-2.1': 'GNU Lesser General Public License.*?1999',
	'LGPL-3.0': 'GNU LESSER GENERAL PUBLIC LICENSE.*?2007',
	'MIT': 'The MIT License',
	'MOZILLA': 'Mozilla Public License',
	'CDDL-1.0': 'COMMON DEVELOPMENT AND DISTRIBUTION LICENSE',
	'ECLIPSE-1.0': 'Eclipse Public License',
}

def usage():
	print '%s -t TOKEN -o OWNER' % (sys.argv[0])

def get_file(url):
	status = 404
	content = ''
	try:
		parts = urlparse.urlparse(url)	
		if parts.scheme == 'https':
			conn = httplib.HTTPSConnection(parts.netloc, parts.port)
		elif parts.scheme == 'http':
			conn = httplib.HTTPConnection(parts.netloc, parts.port)
			
		conn.request('GET', url)
		response = conn.getresponse()
		content = response.read()
		status = response.status
	finally:
		pass

	return status, content
	
def get_license(url):
	try:
		parts = urlparse.urlparse(url)	
		for filename in ['LICENSE', 'LICENSE.txt']:
			status, content = get_file('http://raw.github.com/%s/master/%s' % (parts.path, filename))
			if status == 200:
				for k, v in LICENSES.iteritems():
					if re.search(v, content[:512], re.I | re.S) != None:
						return k
	except Exception, e:
		print e
		sys.stderr.write('%s\n' % (e))
	
	return 'UNKNOWN'

def get_repos(token, owner, cond):
	page = 1
	projects = []
	while True:
		try:
        		conn = httplib.HTTPSConnection('api.github.com', 443)
        		conn.connect()
			url = '/users/%s/starred?direction=desc&sort=created&page=%s' % (owner, page)
			page = page + 1
			sys.stderr.write(':%s\n' % (url))
	                conn.request('GET', url, None, {'Authorization': 'token %s' % (token)})
	                response = conn.getresponse()
			content = response.read()
	                if response.status == 200:
	                	rv = json.loads(content)
				if type(rv) != type([]) or len(rv) == 0:
					break

				for x in rv:
					sys.stderr.write('%s\n' % (x['html_url']))
					if type(x['description']) == type('') and re.search(cond, x['description'], re.I | re.S) != None:
						projects.append(x['html_url'])
					else:
						m = re.match('^.*//github.com/(?P<repo>.*)$', x['html_url'])
						repo = m.group('repo')
						status, content = get_file('https://raw.github.com/%s/master/README.md' % (repo))
						if status == 200 and re.search(cond, content, re.I | re.S) != None:
							projects.append(x['html_url'])
			else:
				break
		except Exception, e:
			print e
			sys.stderr.write('%s\n[E]%s\n' % (url, e))

	return projects
	

def main(argv):
	try:
        	opts, args = getopt.getopt(argv[1:], 't:o:', ['token=', 'owner='])
    	except getopt.GetoptError:
        	usage()
        	sys.exit(2)
	token = ''
	owner = None
	for o, a in opts:
        	if o == '-t':
            		token = a 
		elif o == '-o':
			owner = a

	dataset = []

	projects = []
	if owner == None:
		projects = projects + PROJECTS
	else:
		repos = get_repos(token, owner, 'android')
		fout = open('repos.txt', 'wt')
		fout.write('\n'.join(repos))
		fout.close()
		projects = projects + repos
	
	projects = list(set(projects))

	for x in projects:
		license = get_license(x)

		m = re.match('^.*//github.com/(?P<repo>.*)$', x)
		repo = m.group('repo')
		try:
			sys.stderr.write('url: %s\n' % (x))
			conn = httplib.HTTPSConnection('api.github.com', 443)
			conn.connect()
			conn.request('GET', '/repos/%s' % (repo), None, {'Authorization': 'token %s' % (token)})
			response = conn.getresponse()
			rv = json.loads(response.read())
			if response.status != 200:
				sys.stderr.write('url: %s\nstatus code: %s\nrv: %s\n' % (x, response.status, rv))
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
				'open_issues_count' : open_issues_count,
				'license' : license,
			})
		except Exception, e:
			sys.stderr.write('%s\n[E]%s'%(x, e))
		
	repos = sorted(dataset, key=lambda x: x['forks'], reverse=True)
	for x in repos:
		try:
			print '* [%s](%s)' % (cgi.escape(x['name']), x['html_url']) 
			print
			print '    license:`%s`' % (x['license'])
			print 
			print '    stared:`%s`, forks:`%s`, issues:`%s`, pushed:`%s`' % (x['watchers_count'], x['forks'], x['open_issues_count'], x['pushed_at'])
			print
			print '    %s' % (cgi.escape(x['description']))
			print
		except:
			pass
		
if __name__ == '__main__':
	main(sys.argv)

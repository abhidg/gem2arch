# Python script to parse package_data from gemtoarch
# and print it in a sane manner.

from version import version

def print_pkgbuild(pkgdata, pkgname, pkgver):
	"Dump PKGBUILD of rubygems"

	pkgdata = pkgdata["gems"][pkgname+"-"+pkgver]

	pkgdesc=pkgdata["summary"] if "summary" in pkgdata.keys() else ""
	url=pkgdata["homepage"] if "homepage" in pkgdata.keys() else ""
	depends=["ruby"]

	if "dependencies" in pkgdata.keys():
		for dep in pkgdata["dependencies"]:
			depname = "ruby-" + dep["name"].lower()
			depop =  dep["version_requirements"]["requirements"][0][0]
			depver =  dep["version_requirements"]["requirements"][0][1]["version"]
			if depop == "~>": depop=">"
			depends.append(depname+depop+depver)

	di, depstr = 0,""
	togspace = False
	for dep in depends:
		depstr += "'" + dep + "' "
		di = di + 1
		if di == 4:
			togspace = True
			depstr += "\\\n         "
			di = 0
	depstr = depstr.strip()		
	source = "http://gems.rubyforge.org/gems/%s-$pkgver.gem" % pkgname

	print "# Contributor: gem2arch %s" % version
	print "pkgname=%s" % ("ruby-" + pkgname.lower(),)
	print "pkgver=%s" % pkgver
	print "_realname=\"%s\"" % pkgname
	print "pkgrel=1"
	print "pkgdesc=\"%s\"" % pkgdesc
	print "arch=(any)"
	print "url=\"%s\"" % url
	print "license=()"
	print "depends=(%s)" % depstr
	print "makedepends=(rubygems)"
	print "source=(%s)" % source
	print "noextract=(%s-$pkgver.gem)" % pkgname

	print """
build() {
  cd $srcdir
  local _gemdir="$(ruby -rubygems -e'puts Gem.default_dir')"
  gem install --ignore-dependencies -i "$pkgdir$_gemdir" ${_realname}-$pkgver.gem
}
"""

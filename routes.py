from flask import *
from extensions import connect_to_database
import datetime
import time
import ast
from flask import Flask
from flask import make_response
routes = Blueprint('routes', __name__, template_folder='templates')

linkPrepend = "https://www.inhabitr.com/detail.php?id="

@routes.route('/')
def home_route():
	return render_template("index.html")


@routes.route('/activeListing')
def activeListingRoute():
	db = connect_to_database()
	cur = db.cursor()
	activeInt = 1
	cur.execute("SELECT id, uid, title, address FROM property WHERE status = \"%d\"" %(activeInt))
	propDetails = cur.fetchall()
	allUids = []
	for diction in propDetails:
		allUids.append(diction['uid'])
	userDetails = []
	for uid in allUids:
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		details = cur.fetchone()
		userDetails.append(details)
	what = "activeListing"
	options = {
	"propDetails":propDetails,
	"userDetails":userDetails,
	"what": what
	}

	csv = """"""

	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'Lister Name'"""
	csv += ""","""
	csv += """'Email'"""
	csv += ""","""
	csv += """'Phone'"""
	csv += """\n"""

	for propDet, userDet in zip(propDetails, userDetails):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		nameStr = """%s""" %(str(userDet['first_name'] + " " + userDet['last_name']).replace(',',' '))
		emailStr = """%s""" %(str(userDet['email']).replace(',',' '))
		phoneStr = """%s""" %(str(userDet['mobile']).replace(',',' '))
		
		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += nameStr
		csv += ""","""
		csv += emailStr
		csv += ""","""
		csv += phoneStr
		csv += """\n"""

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response


@routes.route('/inactiveListingRoute')
def inactiveListingRoute():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id, uid, title, address FROM property WHERE status = \"%d\"" %(2))
	deactivateOne = cur.fetchall()
	cur.execute("SELECT id, uid, title, address, filled_type FROM property WHERE status = \"%d\"" %(3))
	filledOne = cur.fetchall()
	cur.execute("SELECT id, uid, title, address FROM property WHERE status = \"%d\"" %(4))
	disAbled = cur.fetchall()
	#cur.execute("SELECT id, uid, title, address FROM property WHERE status = \"%d\"" %(4))
	#toCheck = cur.fetchall()
	# need to confirm how "status = 4" works
	deactivateUids = []
	filledUids = []
	disAbledUids = []
	for diction in deactivateOne:
		deactivateUids.append(diction['uid'])
	for diction in filledOne:
		filledUids.append(diction['uid'])
	for diction in disAbled:
		disAbledUids.append(diction['uid'])
	deactivateUserDetails = []
	filledUserDetails = []
	disabledUserDetails = []
	for uid in deactivateUids:
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		details = cur.fetchone()
		deactivateUserDetails.append(details)
	for uid in filledUids:
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		details = cur.fetchone()
		filledUserDetails.append(details)
	for uid in disAbledUids:
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		details = cur.fetchone()
		disabledUserDetails.append(details)
	what = "inactiveListing"
	options = {
	"deactivated":deactivateOne,
	"filled": filledOne,
	"disabled": disAbled,
	"deacUserDetails": deactivateUserDetails,
	"filledUserDetails": filledUserDetails,
	"disabledUserDetails": disabledUserDetails,
	"what": what
	}

	csv = """"""

	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'Lister Name'"""
	csv += ""","""
	csv += """'Email'"""
	csv += ""","""
	csv += """'Phone'"""
	csv += ""","""
	csv += """'type'"""
	csv += """\n"""

	for propDet, userDet in zip(deactivateOne, deactivateUserDetails):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		nameStr = """%s""" %(str(userDet['first_name'] + " " + userDet['last_name']).replace(',',' '))
		emailStr = """%s""" %(str(userDet['email']).replace(',',' '))
		phoneStr = """%s""" %(str(userDet['mobile']).replace(',',' '))

		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += nameStr
		csv += ""","""
		csv += emailStr
		csv += ""","""
		csv += phoneStr
		csv += ""","""
		csv += """'deactivated'"""
		csv += """\n"""

	for propDet, userDet in zip(filledOne, filledUserDetails):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		nameStr = """%s""" %(str(userDet['first_name'] + " " + userDet['last_name']).replace(',',' '))
		emailStr = """%s""" %(str(userDet['email']).replace(',',' '))
		phoneStr = """%s""" %(str(userDet['mobile']).replace(',',' '))

		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += nameStr
		csv += ""","""
		csv += emailStr
		csv += ""","""
		csv += phoneStr
		csv += ""","""
		if propDet['filled_type'] == 1:
			csv += """'filled by us'"""
		else :
			csv += """'removed by lister'"""
		csv += """\n"""

	for propDet, userDet in zip(disAbled, disabledUserDetails):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		nameStr = """%s""" %(str(userDet['first_name'] + " " + userDet['last_name']).replace(',',' '))
		emailStr = """%s""" %(str(userDet['email']).replace(',',' '))
		phoneStr = """%s""" %(str(userDet['mobile']).replace(',',' '))

		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += nameStr
		csv += ""","""
		csv += emailStr
		csv += ""","""
		csv += phoneStr
		csv += ""","""
		csv += """'disabled'"""
		csv += """\n"""

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response

@routes.route('/inReviewRoute')
def inReviewRoute():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id, uid, title, address FROM property WHERE status = \"%d\"" %(0))
	propDetails = cur.fetchall()
	allUids = []
	for diction in propDetails:
		allUids.append(diction['uid'])
	userDetails = []
	for uid in allUids:
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		details = cur.fetchone()
		userDetails.append(details)
	what = "inReview"
	options = {
	"propDetails":propDetails,
	"userDetails":userDetails,
	"what": what
	}

	csv = """"""

	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'Lister Name'"""
	csv += ""","""
	csv += """'Email'"""
	csv += ""","""
	csv += """'Phone'"""
	csv += """\n"""

	for propDet, userDet in zip(propDetails, userDetails):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		nameStr = """%s""" %(str(userDet['first_name'] + " " + userDet['last_name']).replace(',',' '))
		emailStr = """%s""" %(str(userDet['email']).replace(',',' '))
		phoneStr = """%s""" %(str(userDet['mobile']).replace(',',' '))
		
		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += nameStr
		csv += ""","""
		csv += emailStr
		csv += ""","""
		csv += phoneStr
		csv += """\n"""

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response

@routes.route('/listersContacted')
def listersContactedRoute():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id_from, id_to, id_property, message, created_at, thread FROM message")
	allMessages = cur.fetchall()
	threads = {}
	for message in allMessages:
		threadId = message['thread']
		temp = {}
		temp['id_from'] = message['id_from']
		temp['id_to'] = message['id_to']
		temp['id_property'] = message['id_property']
		temp['message'] = message['message']
		temp['created_at'] = message['created_at']
		if threadId in threads:
			threads[threadId].append(temp)
		else:
			threads[threadId] = []
			threads[threadId].append(temp)
	listersContacted = []
	listersWhoContacted = []
	seekersContacted = []
	seekersWhoContacted = []
	props = []
	messageThread = []
	threadFrom = []
	order= []
	for key, val in threads.items():
		firstMessage = val[0]
		propId = int(firstMessage['id_property'])
		cur.execute("SELECT enable_booking, can_book FROM property WHERE id = \"%d\"" %(propId))
		Det = cur.fetchone()
		enable = Det['enable_booking']
		booked = Det['can_book']

		if enable == 0 or (enable == 1 and booked == 0):


			listerId = int(firstMessage['id_to'])
			seekerId = int(firstMessage['id_from'])
		

			cur.execute("SELECT uid FROM property WHERE id = \"%d\"" %(propId))
			idDet = cur.fetchone()
			userId = idDet['uid']
		
			cur.execute("SELECT first_name, last_name, email, mobile from landlord WHERE id = \"%d\"" %(listerId))
			listerDet = cur.fetchone()
			if listerId == userId:
				order.append("lister")
				listersContacted.append(listerDet)
			else:
				order.append("seeker")
				seekersContacted.append(listerDet)

			cur.execute("SELECT first_name, last_name, email, mobile from landlord WHERE id = \"%d\"" %(seekerId))
			seekerDet = cur.fetchone()
			if listerId == userId:
				seekersWhoContacted.append(seekerDet)
			else:
				listersWhoContacted.append(seekerDet)


			cur.execute("SELECT id, title, address FROM property WHERE id = \"%d\"" %(propId))
			propDet = cur.fetchone()
			props.append(propDet)

			temp = []
			messFrom = []
			for mess in val:
				fromId = mess['id_from']
				if fromId == str(userId):
					messFrom.append("lister")
				else:
					messFrom.append("seeker")
				messClean = mess['message']
				temp.append(messClean)
			threadFrom.append(messFrom)
			messageThread.append(temp)

	what = "contacted"
	options = {
	"listers":listersContacted,
	"listersWhoContacted": listersWhoContacted,
	"seekersContacted": seekersContacted,
	"seekers":seekersWhoContacted,
	"threads":messageThread,
	"propDetails": props,
	"order": order,
	"what": what
	}

	csv = """"""

	csv += """'from-to'"""
	csv += ""","""
	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'FromName'"""
	csv += ""","""
	csv += """'FromEmail'"""
	csv += ""","""
	csv += """'FromPhone'"""
	csv += ""","""
	csv += """'ToName'"""
	csv += ""","""
	csv += """'ToEmail'"""
	csv += ""","""
	csv += """'ToPhone'"""
	csv += ""","""
	csv += """'Thread'"""
	csv += """\n"""

	listToSeekInd = 0
	seekToListInd = 0

	for propDet, mThread, fromThread, orderDet in zip(props, messageThread, threadFrom, order):
		propId = propDet['id']
		linkStr = """%s""" %(linkPrepend+str(propId))
		titleStr = """%s""" %(str(propDet['title']).replace(',',' '))
		addrStr = """%s""" %(str(propDet['address']).replace(',',' '))
		fromNameStr = None
		fromEmailStr = None
		fromPhoneStr = None
		
		ToNameStr = None
		toEmailStr = None
		toPhoneStr = None

		fromToStr = None

		if orderDet == "lister":

			fromToStr = "seeker to lister"

			fromNameStr = """%s""" %(str(seekersWhoContacted[seekToListInd]['first_name'] + " " + seekersWhoContacted[seekToListInd]['last_name']).replace(',',' '))
			fromEmailStr = """%s""" %(str(seekersWhoContacted[seekToListInd]['email']).replace(',',' '))
			fromPhoneStr = """%s""" %(str(seekersWhoContacted[seekToListInd]['mobile']).replace(',',' '))

			ToNameStr = """%s""" %(str(listersContacted[seekToListInd]['first_name'] + " " + listersContacted[seekToListInd]['last_name']).replace(',',' '))
			toEmailStr = """%s""" %(str(listersContacted[seekToListInd]['email']).replace(',',' '))
			toPhoneStr = """%s""" %(str(listersContacted[seekToListInd]['mobile']).replace(',',' '))

			seekToListInd += 1
		else:

			fromToStr = "lister to seeker"

			fromNameStr = """%s""" %(str(listersWhoContacted[listToSeekInd]['first_name'] + " " + listersWhoContacted[listToSeekInd]['last_name']).replace(',',' '))
			fromEmailStr = """%s""" %(str(listersWhoContacted[listToSeekInd]['email']).replace(',',' '))
			fromPhoneStr = """%s""" %(str(listersWhoContacted[listToSeekInd]['mobile']).replace(',',' '))

			ToNameStr = """%s""" %(str(seekersContacted[listToSeekInd]['first_name'] + " " + seekersContacted[listToSeekInd]['last_name']).replace(',',' '))
			toEmailStr = """%s""" %(str(seekersContacted[listToSeekInd]['email']).replace(',',' '))
			toPhoneStr = """%s""" %(str(seekersContacted[listToSeekInd]['mobile']).replace(',',' '))

			listToSeekInd += 1

		threadStr = ""
		for message, fromPerson in zip(mThread, fromThread):
			threadStr += str(fromPerson)
			threadStr += ": "
			mess = str(message)
			mess = mess.replace(',','.')
			mess = mess.replace('\r',' ').replace('\n',' ')
			threadStr += mess
			threadStr += "  "

		allThread = str(threadStr).replace(',','.')
		allThread = allThread.replace('\r',' ').replace('\n',' ')
		allThread = """%s""" %(str(allThread))


		csv += fromToStr
		csv += ""","""
		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += fromNameStr
		csv += ""","""
		csv += fromEmailStr
		csv += ""","""
		csv += fromPhoneStr
		csv += ""","""
		csv += ToNameStr
		csv += ""","""
		csv += toEmailStr
		csv += ""","""
		csv += toPhoneStr
		csv += ""","""
		csv += allThread
		csv += """\n"""

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response


@routes.route('/listersContactedBookNow')
def listersContactedBookNow():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id_from, id_to, id_property, message, created_at, thread FROM message")
	allMessages = cur.fetchall()
	one = {}
	for message in allMessages:
		idFrom = int(message['id_from'])
		idTo = int(message['id_to'])
		propId = int(message['id_property'])
		lid = 0
		sid = 0
		cur.execute("SELECT * from property WHERE uid = \"%d\" and id = \"%d\"" %(idFrom, propId))
		result = cur.fetchone()
		if result is None:
			sid = idFrom
			lid = idTo
		else:
			sid = idTo
			lid = idFrom
		key = str(lid)+"-"+str(sid)+"-"+str(propId)
		temp = {}
		temp['lid'] = lid
		temp['sid'] = sid
		if idFrom == sid:
			temp['user'] = "seeker"
		else:
			temp['user'] = "lister"
		temp['message'] = message['message']
		temp['created_at'] = message['created_at']
		temp['pid'] = propId
		cur.execute("SELECT created_at FROM bookings WHERE uid = \"%d\" and pid = \"%d\"" %(sid,propId))
		result = cur.fetchone()
		if result is None:
			temp['booking'] = "not yet booked"
		else:
			if message['created_at'] < result['created_at']:
				temp['booking'] = "before"
			else:
				temp['booking'] = "after"

		if key in one:
			one[key].append(temp)
		else:
			one[key] = []
			one[key].append(temp)

	cur.execute("SELECT lid, sid, bid, user, message, created_at FROM booking_queries")
	bookQueries = cur.fetchall()
	threads = {}
	propDetails = []
	listersWhoContacted = []
	seekersContacted = []
	listersContacted = []
	seekersWhoContacted = []
	order = []
	messageThread = []
	before_after = []
	fromTo = []
	fromThread = []

	for diction in bookQueries:
		lid = str(diction['lid'])
		sid = str(diction['sid'])
		bId = diction['bid']
		cur.execute("SELECT pid FROM bookings WHERE id = \"%d\"" %(bId))
		propDet = cur.fetchone()
		propId = str(propDet['pid'])
		key = lid+"-"+sid+"-"+propId

		temp = {}
		temp['lid'] = diction['lid']
		temp['sid'] = diction['sid']
		temp['user'] = diction['user']
		temp['message'] = diction['message']
		temp['created_at'] = diction['created_at']
		temp['booking'] = "after"
		temp['pid'] = propId
		if key in threads:
			threads[key].append(temp)
		else:
			threads[key] = []
			threads[key].append(temp)

	for key,val in one:
		if key in threads:
			mergeList = val+threads[key]
			newList = sorted(mergeList, key=lambda k: k['created_at'])
			one[key] = newList
	for key, val in threads:
		if key in one:
			x = 0
		else:
			one[key] = val 


	for key, val in one:
		firstMessage = val[0]
		pid = firstMessage['pid']
		cur.execute("SELECT enable_booking, can_book FROM property WHERE id = \"%d\"" %(pid))
		Det = cur.fetchone()
		enable = Det['enable_booking']
		booked = Det['can_book']

		if enable == 1 and booked == 1:

			cur.execute("SELECT id, title, address FROM property WHERE id = \"%d\"" %(pid))
			pDet = cur.fetchone()
			propDetails.append(pDet)

			lId = firstMessage['lid']
			sId = firstMessage['sid']
			user = firstMessage['user']
		
			cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(lId))
			listerDet = cur.fetchone()
			cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(sId))
			seekerDet = cur.fetchone()

			if user == "lister":
				fromTo.append("lister to seeker")
				listersWhoContacted.append(listerDet)
				seekersContacted.append(seekerDet)
				order.append("seeker")
			else:
				fromTo.append("seeker to lister")
				seekersWhoContacted.append(seekerDet)
				listersContacted.append(listerDet)
				order.append("lister")

			temp = []
			tempTwo = []
			tempThree = []
			for mess in val:
				fromPerson = mess['user']
				tempThree.append(fromPerson)
				messClean = mess['message']
				tempTwo.append(mess['booking'])
				temp.append(messClean)
			fromThread.append(tempThree)
			messageThread.append(temp)
			before_after.append(tempTwo)

	what = "contact with booking"

	options = {
	"propDetails": propDetails,
	"listersContacted":listersContacted,
	"seekersContacted":seekersContacted,
	"listersWhoContacted":listersWhoContacted,
	"seekersWhoContacted":seekersWhoContacted,
	"threads":messageThread,
	"order":order,
	"what":what,
	"before_after":before_after,
	"fromToDet": fromTo
	}

	csv = """"""

	csv += """'before/after booknow'"""
	csv += ""","""
	csv += """'from-to'"""
	csv += ""","""
	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'FromName'"""
	csv += ""","""
	csv += """'FromEmail'"""
	csv += ""","""
	csv += """'FromPhone'"""
	csv += ""","""
	csv += """'ToName'"""
	csv += ""","""
	csv += """'ToEmail'"""
	csv += ""","""
	csv += """'ToPhone'"""
	csv += ""","""
	csv += """'Thread'"""
	csv += """\n"""

	fromNameStr = None
	fromEmailStr = None
	fromPhoneStr = None

	toNameStr = None
	toEmailStr = None
	toPhoneStr = None

	for prop, thread, orderDet, fromToDet, beforeAfterDet, fromPersons in zip(propDetails, messageThread, order, fromTo, before_after, fromThread):
		pId = prop['id']
		linkStr = """%s""" %(linkPrepend + str(pId))
		titleStr = """%s""" %(str(prop['title']).replace(',','.').replace('\n',' '))
		addrStr = """%s""" %(strprop['address'].replace(',','.').replace('\n',' '))
		fromToStr = """%s""" %(fromToDet)
		beforeAfterStr = """%s""" %(beforeAfterDet[0])

		listToSeekInd = 0
		seekToListInd = 0

		if orderDet == "lister":
			toNameStr ="""%s"""  %(str(listersContacted[seekToListInd]['first_name'] + " "+ listersContacted[seekToListInd]['last_name']).replace(',','.').replace('\n',' '))
			toEmailStr = """%s""" %(str(listersContacted[seekToListInd]['email']).replace(',','.').replace('\n',' '))
			toPhoneStr = """%s""" %(str(listersContacted[seekToListInd]['mobile']).replace(',','.').replace('\n',' '))

			fromNameStr ="""%s"""  %(str(seekersWhoContacted[seekToListInd]['first_name'] + " "+ seekersWhoContacted[seekToListInd]['last_name']).replace(',','.').replace('\n',' '))
			fromEmailStr = """%s""" %(str(seekersWhoContacted[seekToListInd]['email']).replace(',','.').replace('\n',' '))
			fromPhoneStr = """%s""" %(str(seekersWhoContacted[seekToListInd]['mobile']).replace(',','.').replace('\n',' '))

			seekToListInd += 1

		else:
			toNameStr ="""%s"""  %(str(seekersContacted[listToSeekInd]['first_name'] + " "+ seekersContacted[listToSeekInd]['last_name']).replace(',','.').replace('\n',' '))
			toEmailStr = """%s""" %(str(seekersContacted[listToSeekInd]['email']).replace(',','.').replace('\n',' '))
			toPhoneStr = """%s""" %(str(seekersContacted[listToSeekInd]['mobile']).replace(',','.').replace('\n',' '))

			fromNameStr ="""%s"""  %(str(listersWhoContacted[listToSeekInd]['first_name'] + " "+ listersWhoContacted[listToSeekInd]['last_name']).replace(',','.').replace('\n',' '))
			fromEmailStr = """%s""" %(str(listersWhoContacted[listToSeekInd]['email']).replace(',','.').replace('\n',' '))
			fromPhoneStr = """%s""" %(str(listersWhoContacted[listToSeekInd]['mobile']).replace(',','.').replace('\n',' '))

			listToSeekInd += 1

		threadStr = ""
		for mess, fromPerson, befAft in zip(thread, fromPersons, beforeAfterDet):
			threadStr += str(fromPerson)
			threadStr += "("
			threadStr += styr(befAft)
			threadStr += "): "
			threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r', ' ')
			threadStr += "  "

		allThread = """%s""" %(str(threadStr).replace(',','.').replace('\n',' ').replace('\r',' '))

		csv += fromToStr
		csv += ""","""
		csv += beforeAfterStr
		csv += ""","""
		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += fromNameStr
		csv += ""","""
		csv += fromEmailStr
		csv += ""","""
		csv += fromPhoneStr
		csv += ""","""
		csv += toNameStr
		csv += ""","""
		csv += toEmailStr
		csv += ""","""
		csv += toPhoneStr
		csv += ""","""
		csv += allThread
		csv += "\n"

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response

@routes.route('/notRespondingBookNow')
def notRespondingBookNow():
	db = connect_to_database()
	cur = db.cursor()
	one = {}
	cur.execute("SELECT id_from, id_to, id_property, message, created_at, thread FROM message")
	allMessages = cur.fetchall()
	for message in allMessages:
		temp = {}
		lid = 0
		sid = 0
		idFrom = mesage['id_from']
		idTo = message['id_to']
		propId = message['id_property']
		cur.execute("SELECT * FROM property WHERE uid = \"%d\" and id = \"%d\"" %(idFrom, propId))
		result = cur.fetchone()
		if result is None:
			sid = idFrom
			lid = idTo
		else:
			sid = idTo
			lid = idFrom
		temp['pid'] = propId
		temp['lid'] = lid
		temp['sid'] = sid
		if idFrom == sid:
			temp['user'] = "seeker"
		else:
			temp['user'] = "lister"
		temp['message'] = message['message']
		temp['created_at'] = message['created_at']
		cur.execute("SELECT created_at FROM bookings WHERE uid = \"%d\" and pid = \"%d\"" %(sid,propId))
		result = cur.fetchone()
		if result is None:
			temp['booking'] = "not yet booked"
		else:
			if result['created_at'] <= message['created_at']:
				temp['booking'] = "after"
			else:
				temp['booking'] = "before"
		key = str(lid)+"-"+str(sid)+"-"+str(propId)
		if key in one:
			one[key].append(temp)
		else:
			one[key] = []
			one[key].append(temp)

	cur.execute("SELECT sid, lid, bid, user, message, created_at FROM booking_queries")
	allMessages = cur.fetchall()
	threads = {}
	for message in allMessages:
		bId = message['bid']
		temp = {}
		temp['lid'] = message['lid']
		temp['sid'] = message['sid']
		temp['user'] = message['user']
		temp['message'] = message['message']
		temp['created_at'] = message['created_at']
		temp['booking'] = "after"
		cur.execute("SELECT pid FROM bookings WHERE id = \"%d\"" %(bId))
		propDet = cur.fetchone()
		propId = propDet['pid']
		temp['pid'] = propId
		key = str(lid)+"-"+str(sid)+"-"+str(propId)
		if key in threads:
			threads[key].append(temp)
		else:
			threads[key] = []
			threads[key].append(temp)
	listerNoResponseFirst = []
	seekerNoResponseFirst = []
	listerNoResponseSecond = []
	seekerNoResponseSecond = []
	propDetails = []
	order = []

	for key, val in one:
		if key in threads:
			mergeList = val+threads[key]
			newList = sorted(mergeList, key=lambda k: k['created_at'])
			one[key] = newList
	for key, value in threads:
		if key in one:
			x = 0
		else:
			one[key] = val


	for key, val in one:
		firstMessage = val[0]
		pId = firstMessage['pid']
		cur.execute("SELECT enable_booking, can_book FROM property WHERE id = \"%d\"" %(pId))
		Det = cur.fetchone()
		enable = Det['enable_booking']
		booked = Det['can_book']

		if enable == 1 and booked == 1:

			first = firstMessage['user']
			lId = firstMessage['lid']
			sId = firstMessage['sid']
			secondResponds = 0
			firstResponds = 0
			for message in val:
				if firstResponds == 1:
					break;
				if message['user'] != first:
					secondResponds = 1
				if secondResponds == 1 and message['user'] == user:
					firstResponds = 1
			if firstResponds == 1:
				x = 0
			elif secondResponds == 1 and firstResponds == 0:
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(lId))
				listerDet = cur.fetchone()
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(sId))
				seekerDet = cur.fetchone()
				cur.execute("SELECT id, title, address FROM property WHERE id = \"%d\"" %(pId))
				propDet = cur.fetchone()
				messageThread = []
				before_after = []
				fromThread = []
				for mess in val:
					fromThread.append(mess['user'])
					before_after.append(mess['booking'])
					messClean = mess['message']
					messageThread.append(messClean)
				lastInd = len(val)-1
				lastMessage = val[lastInd]
				lastMessTime = lastMessage['created_at']
				currTime = time.time()
				currDt = datetime.datetime.fromtimestamp(currTime)
				lastDt = datetime.datetime.fromtimestamp(lastMessTime)
				timeElapsed = currDt-lastDt
				temp = {}
				temp['listerDet'] = listerDet
				temp['seekerDet'] = seekerDet
				temp['propDet'] = propDet
				temp['thread'] = messageThread
				temp['elapsed'] = timeElapsed
				temp['before_after'] = before_after
				temp['fromThread'] = fromThread
				if first == "lister":
					listerNoResponseSecond.append(temp)
					order.append("listerSecond")
				else:
					order.append("seekerSecond")
					seekerNoResponseSecond.append(temp)
			elif secondResponds == 0:
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(lId))
				listerDet = cur.fetchone()
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(sId))
				seekerDet = cur.fetchone()
				cur.execute("SELECT id, title, address FROM property WHERE id = \"%d\"" %(pId))
				propDet = cur.fetchone()
				messageThread = []
				before_after = []
				for mess in val:
					before_after.append(mess['booking'])
					fromThread.append(mess['user'])
					messClean = mess['message']
					messageThread.append(messClean)
				lastInd = len(val)-1
				lastMessage = val[lastInd]
				lastMessTime = lastMessage['created_at']
				currTime = time.time()
				currDt = datetime.datetime.fromtimestamp(currTime)
				lastDt = datetime.datetime.fromtimestamp(lastMessTime)
				timeElapsed = currDt-lastDt
				temp = {}
				temp['listerDet'] = listerDet
				temp['seekerDet'] = seekerDet
				temp['propDet'] = propDet
				temp['thread'] = messageThread
				temp['elapsed'] = timeElapsed
				temp['before_after'] = before_after
				temp['fromThread'] = fromThread
				if first == "lister":
					order.append("seekerFirst")
					seekerNoResponseFirst.append(temp)
				else:
					order.append("listerFirst")
					listerNoResponseFirst.append(temp)
	what = "noResponseBookNow"
	options = {
	"listerFirst":listerNoResponseFirst,
	"listerSecond":listerNoResponseSecond,
	"seekerFirst":seekerNoResponseFirst,
	"seekerSecond":seekerNoResponseSecond,
	"what":what,
	"order":order
	}

	csv = """"""

	csv += """'Type'"""
	csv += ""","""
	csv += """'Stopped When'"""
	csv += ""","""
	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'ListerName'"""
	csv += ""","""
	csv += """'ListerEmail'"""
	csv += ""","""
	csv += """'ListerPhone'"""
	csv += ""","""
	csv += """'SeekerName'"""
	csv += ""","""
	csv += """'SeekerEmail'"""
	csv += ""","""
	csv += """'SeekerPhone'"""
	csv += ""","""
	csv += """'Elapsed'"""
	csv += ""","""
	cvs += """'Thread'"""
	csv += """\n"""

	listerFirstInd = 0
	listerSecondInd = 0
	seekerFirstInd = 0
	seekerSecondInd = 0

	for orderDet in order:
		typeStr = None
		stoppedStr = None
		linkStr = None
		titleStr = None
		addrStr = None
		lNameStr = None
		lEmailStr = None
		lPhoneStr = None
		sNameStr = None
		sEmailStr = None
		sPhoneStr = None
		elapsedStr = None
		threadStr = None
		if orderDet == "listerFirst":
			typeStr = """%s""" %(typeStr)
			linkStr = """%s""" %(str(linkPrepend+str(listersFirst[listerFirstInd]['propDet']['id'])).replace(',','.'))
			titleStr = """%s""" %(str(listersFirst[listerFirstInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(listerFirst[listerFirstInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['first_name']+" "+listersFirst[listerFirstInd]['listerDet']['last_name']).replace(',','.'))
			lEmailStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['first_name']+" "+listersFirst[listerFirstInd]['seekerDet']['last_name']).replace(',','.'))
			sEmailStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(listersFirst[listerFirstInd]['elapsed']).replace(',','.'))

			messThread = listersFirst[listerFirstInd]['thread']
			fromThread = listersFirst[listerFirstInd]['fromThread']
			beforeAfterThread = listersFirst[listerFirstInd]['before_after']

			threadStr = ""
			for mess, fromPerson, befAft in zip(messThread, fromThread, beforeAfterThread):
				threadStr += fromPerson
				threadStr += "("
				threadStr += befAft
				threadStr += ")"
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "

			listerFirstInd += 1
		elif orderDet == "listerSecond":
			typeStr = """%s""" %(typeStr)
			linkStr = """%s""" %(str(linkPrepend+str(listersSecond[listerSecondInd]['propDet']['id'])).replace(',','.'))
			titleStr = """%s""" %(str(listersSecond[listerSecondInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(listerSecond[listerSecondInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['first_name']+" "+listersSecond[listerSecondInd]['listerDet']['last_name']).replace(',','.'))
			lEmailStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['first_name']+" "+listersSecond[listerSecondInd]['seekerDet']['last_name']).replace(',','.'))
			sEmailStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(listersSecond[listerSecondInd]['elapsed']).replace(',','.'))

			messThread = listersSecond[listerSecondInd]['thread']
			fromThread = listersSecond[listerSecondInd]['fromThread']
			beforeAfterThread = listersSecond[listerSecondInd]['before_after']

			threadStr = ""
			for mess, fromPerson, befAft in zip(messThread, fromThread, beforeAfterThread):
				threadStr += fromPerson
				threadStr += "("
				threadStr += befAft
				threadStr += ")"
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "

			listerSecondInd += 1
		elif orderDet == "seekerFirst":
			typeStr = """%s""" %(typeStr)
			linkStr = """%s""" %(str(linkPrepend+str(seekersFirst[seekerFirstInd]['propDet']['id'])).replace(',','.'))
			titleStr = """%s""" %(str(seekersFirst[seekerFirstInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(seekersFirst[seekerFirstInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['first_name']+" "+seekersFirst[seekerFirstInd]['listerDet']['last_name']).replace(',','.'))
			lEmailStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['first_name']+" "+seekersFirst[seekerFirstInd]['seekerDet']['last_name']).replace(',','.'))
			sEmailStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(seekersFirst[seekerFirstInd]['elapsed']).replace(',','.'))

			messThread = seekersFirst[seekerFirstInd]['thread']
			fromThread = seekersFirst[seekerFirstInd]['fromThread']
			beforeAfterThread = seekersFirst[seekerFirstInd]['before_after']

			threadStr = ""
			for mess, fromPerson, befAft in zip(messThread, fromThread, beforeAfterThread):
				threadStr += fromPerson
				threadStr += "("
				threadStr += befAft
				threadStr += ")"
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "

			listerFirstInd += 1














	return render_template("new.html", **options)


@routes.route('/listersRespondingRoute')
def notRespondingRoute():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id_from, id_to, id_property, message, created_at, thread FROM message")
	allMessages = cur.fetchall()
	threads = {}
	for message in allMessages:
		threadId = message['thread']
		temp = {}
		temp['id_from'] = message['id_from']
		temp['id_to'] = message['id_to']
		temp['id_property'] = message['id_property']
		temp['message'] = message['message']
		temp['created_at'] = message['created_at']
		if threadId in threads:
			threads[threadId].append(temp)
		else:
			threads[threadId] = []
			threads[threadId].append(temp)
	seekerNoResponseFirst = []
	seekerNoResponseSecond = []
	listerNoResponseFirst = []
	listerNoResponseSecond = []
	props = []
	order = []
	for key, val in threads.items():
		firstMessage = val[0]

		pid = firstMessage['id_property']

		cur.execute("SELECT enable_booking, can_book FROM property WHERE id = \"%d\"" %(pid))
		Det = cur.fetchone()
		enable = Det['enable_booking']
		booked = Det['can_book']

		if enable == 0 or (enable == 1 and booked == 0):


			listerId = int(firstMessage['id_to'])
			seekerId = int(firstMessage['id_from'])
			propId = int(firstMessage['id_property'])

			cur.execute("SELECT uid FROM property WHERE id = \"%d\"" %(propId))
			idDet = cur.fetchone()
			userId = idDet['uid']

			cur.execute("SELECT id, title, address FROM property WHERE id = \"%d\"" %(propId))
			propDet = cur.fetchone()
			props.append(propDet)


			listerResponds = 0
			seekerResponds = 0

			for message in val:
				if seekerResponds == 1:
					break
				if int(message['id_from']) == listerId and int(message['id_to']) == seekerId:
					listerResponds = 1
				if listerResponds == 1 and int(message['id_from']) == seekerId and int(message['id_to']) == listerId:
					seekerResponds = 1

			if seekerResponds == 1:
				a = 3
			elif listerResponds == 1 and seekerResponds == 0:
				temp = {}
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(listerId))
				listerDet = cur.fetchone()
				temp['listerDet'] = listerDet
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(seekerId))
				seekerDet = cur.fetchone()
				temp['seekerDet'] = seekerDet
				cur.execute("SELECT id, title, address FROM property WHERE id = \"%s\"" %(propId))
				propDet = cur.fetchone()
				temp['propDet'] = propDet
				messageThread = []
				fromData = []

				for mess in val:
					idFrom = int(mess['id_from'])
					if idFrom == userId:
						fromData.append("lister")
					else:
						fromData.append("seeker")
					messClean = mess['message']
					messageThread.append(messClean)
				temp['fromData'] = fromData
				temp['messageThread'] = messageThread
				lastInd = len(val)-1
				lastMessage = val[lastInd]
				lastMessTime = lastMessage['created_at']
				currTime = time.time()
				currDt = datetime.datetime.fromtimestamp(currTime)
				lastDt = datetime.datetime.fromtimestamp(lastMessTime)
				timeElapsed = currDt-lastDt
				temp['elapsed'] = timeElapsed
				if listerId == userId:
					seekerNoResponseSecond.append(temp)
					order.append("listerSecond")
				else:
					listerNoResponseSecond.append(temp)
					order.append("seekerSecond")
			elif listerResponds == 0:
				temp = {}
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(listerId))
				listerDet = cur.fetchone()
				temp['listerDet'] = listerDet
				cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(seekerId))
				seekerDet = cur.fetchone()
				temp['seekerDet'] = seekerDet
				cur.execute("SELECT id, title, address FROM property WHERE id = \"%s\"" %(propId))
				propDet = cur.fetchone()
				temp['propDet'] = propDet
				messageThread = []
				fromData = []
				for mess in val:
					idFrom = int(mess['id_from'])
					if idFrom == userId:
						fromData.append("lister")
					else:
						fromData.append("seeker")
					messClean = mess['message']
					messageThread.append(messClean)
				temp['fromData'] = fromData
				temp['messageThread'] = messageThread
				lastInd = len(val)-1
				lastMessage = val[lastInd]
				lastMessTime = lastMessage['created_at']
				currTime = time.time()
				currDt = datetime.datetime.fromtimestamp(currTime)
				lastDt = datetime.datetime.fromtimestamp(lastMessTime)
				timeElapsed = currDt-lastDt
				temp['elapsed'] = timeElapsed
				if listerId == userId:
					listerNoResponseFirst.append(temp)
					order.append("listerFirst")
				else:
					seekerNoResponseFirst.append(temp)
					order.append("seekerFirst")
	what = "noResponse"
	options = {
	"listersFirst": listerNoResponseFirst,
	"seekersFirst": seekerNoResponseFirst,
	"listersSecond": listerNoResponseSecond,
	"seekersSecond": seekerNoResponseSecond,
	"propertyDetails":props,
	"order":order,
	"what": what
	}

	listerFirstInd = 0
	listerSecondInd = 0
	seekerFirstInd = 0
	seekerSecondInd = 0

	csv = """"""

	csv += """'Type'"""
	csv += ""","""
	csv += """'Link'"""
	csv += ""","""
	csv += """'Title'"""
	csv += ""","""
	csv += """'Address'"""
	csv += ""","""
	csv += """'ListerName'"""
	csv += ""","""
	csv += """'ListerEmail'"""
	csv += ""","""
	csv += """'ListerPhone'"""
	csv += ""","""
	csv += """'SeekerName'"""
	csv += ""","""
	csv += """'SeekerEmail'"""
	csv += ""","""
	csv += """'SeekerPhone'"""
	csv += ""","""
	csv += """'Elapsed'"""
	csv += ""","""
	csv += """'Thread'"""
	csv += """\n"""

	for orderDet in order:
		typeStr = None
		linkStr = None
		titleStr = None
		addrStr = None
		lNameStr = None
		lEmailStr = None
		lPhoneStr = None
		sNameStr = None
		sEmailStr = None
		sPhoneStr = None
		threadStr = None
		
		if orderDet == "listerFirst":
			typeStr = """%s""" %(orderDet)
			linkStr = """%s""" %(str(linkPrepend+str(listersFirst[listerFirstInd]['propDet']['id'])))
			titleStr = """%s""" %(str(listersFirst[listerFirstInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(listersFirst[listerFirstInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['first_name']+" "+listersFirst[listerFirstInd]['listerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lEmailStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(listersFirst[listerFirstInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['first_name']+" "+listersFirst[listerFirstInd]['seekerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			sEmailStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(listersFirst[listerFirstInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(listersFirst[listerFirstInd]['elapsed']).replace(',','.'))

			messThread = listersFirst[listerFirstInd]['messageThread']
			fromThread = listersFirst[listerFirstInd]['fromData']

			threadStr = ""
			for mess,fromDet in zip(messThread,fromThread):
				threadStr += fromDet
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "
			listerFirstInd += 1
		elif orderDet == "listerSecond":
			typeStr = """%s""" %(orderDet)
			linkStr = """%s""" %(str(linkPrepend+str(listersSecond[listerSecondInd]['propDet']['id'])))
			titleStr = """%s""" %(str(listersSecond[listerSecondInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(listersSecond[listerSecondInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['first_name']+" "+listersSecond[listerSecondInd]['listerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lEmailStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(listersSecond[listerSecondInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['first_name']+" "+listersSecond[listerSecondInd]['seekerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			sEmailStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(listersSecond[listerSecondInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(listersSecond[listerSecondInd]['elapsed']).replace(',','.'))

			messThread = listersSecond[listerSecondInd]['messageThread']
			fromThread = listersSecond[listerSecondInd]['fromData']

			threadStr = ""
			for mess,fromDet in zip(messThread,fromThread):
				threadStr += fromDet
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "
			listerSecondInd += 1
		elif orderDet == "seekerFirst":
			typeStr = """%s""" %(orderDet)
			linkStr = """%s""" %(str(linkPrepend+str(seekersFirst[seekerFirstInd]['propDet']['id'])))
			titleStr = """%s""" %(str(seekersFirst[seekerFirstInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(seekersFirst[seekerFirstInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['first_name']+" "+seekersFirst[seekerFirstInd]['listerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lEmailStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(seekersFirst[seekerFirstInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['first_name']+" "+seekersFirst[seekerFirstInd]['seekerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			sEmailStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(seekersFirst[seekerFirstInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(seekersFirst[seekerFirstInd]['elapsed']).replace(',','.'))

			messThread = seekersFirst[seekerFirstInd]['messageThread']
			fromThread = seekersFirst[seekerFirstInd]['fromData']

			threadStr = ""
			for mess,fromDet in zip(messThread,fromThread):
				threadStr += fromDet
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "
			seekerFirstInd += 1
		elif orderDet == "seekerSecond":
			typeStr = """%s""" %(orderDet)
			linkStr = """%s""" %(str(linkPrepend+str(seekersSecond[seekerSecondInd]['propDet']['id'])))
			titleStr = """%s""" %(str(seekersSecond[seekerSecondInd]['propDet']['title']).replace(',','.').replace('\n',' ').replace('\r',' '))
			addrStr = """%s""" %(str(seekersSecond[seekerSecondInd]['propDet']['address']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lNameStr = """%s""" %(str(seekersSecond[seekerSecondInd]['listerDet']['first_name']+" "+seekersSecond[seekerSecondInd]['listerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			lEmailStr = """%s""" %(str(seekersSecond[seekerSecondInd]['listerDet']['email']).replace(',','.'))
			lPhoneStr = """%s""" %(str(seekersSecond[seekerSecondInd]['listerDet']['mobile']).replace(',','.'))
			sNameStr = """%s""" %(str(seekersSecond[seekerSecondInd]['seekerDet']['first_name']+" "+seekersSecond[seekerSecondInd]['seekerDet']['last_name']).replace(',','.').replace('\n',' ').replace('\r',' '))
			sEmailStr = """%s""" %(str(seekersSecond[seekerSecondInd]['seekerDet']['email']).replace(',','.'))
			sPhoneStr = """%s""" %(str(seekersSecond[seekerSecondInd]['seekerDet']['mobile']).replace(',','.'))
			elapsedStr = """%s""" %(str(seekersSecond[seekerSecondInd]['elapsed']).replace(',','.'))

			messThread = seekersSecond[seekerSecondInd]['messageThread']
			fromThread = seekersSecond[seekerSecondInd]['fromData']

			threadStr = ""
			for mess,fromDet in zip(messThread,fromThread):
				threadStr += fromDet
				threadStr += ": "
				threadStr += str(mess).replace(',','.').replace('\n',' ').replace('\r',' ')
				threadStr += "  "
			seekerSecondInd += 1

		csv += typeStr
		csv += ""","""
		csv += linkStr
		csv += ""","""
		csv += titleStr
		csv += ""","""
		csv += addrStr
		csv += ""","""
		csv += lNameStr
		csv += ""","""
		csv += lEmailStr
		csv += ""","""
		csv += lPhoneStr
		csv += ""","""
		csv += sNameStr
		csv += ""","""
		csv += sEmailStr
		csv += ""","""
		csv += sPhoneStr
		csv += ""","""
		csv += elapsedStr
		csv == ""","""
		csv += threadStr
		csv += """\n"""

	response = make_response(csv)
	response.headers["Content-Disposition"] = "attachment; filename=activeListings.csv"
	return response


@routes.route('/bookingNotEnabledRoute')
def bookingNotEnabled():
	startTime = 1493741541
	db = connect_to_database()
	cur = db.cursor()
	one = 1
	zero = 0
	cur.execute("SELECT id, uid, title, address from property WHERE enable_booking = \"%d\" and can_book == \"%d\"" %(one,zero))
	notEnabledListings = cur.fetchall()
	userDetails = []
	for diction in notEnabledListings:
		uid = diction['uid']
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uid))
		tempDict = cur.fetchone()
		userDetails.append(tempDict)
	what = "not enabled" 
	options = {
	"propDetails": notEnabledListings,
	"userDetails": userDetails,
	"what": what
	}
	return render_template("new.html", **options)

# need to talk to Ali to finish this
# @routes.route('/bookingEnabledRoute')
# def enabledDetails():
# 	startTime = 1493741541
# 	db = connect_to_database()
# 	cur = db.cursor()
# 	one = 1
# 	zero = 0
# 	cur.execute("SELECT id, uid, title, address,  from property WHERE enable_booking = \"%d\" and can_book == \"%d\"" %(one,one))
# 	enabledListings = cur.fetchall()

	
# uynderstand where all the req documents are recorded


@routes.route('/firstContactRoute')
def daysForFirstContact():
	city = request.args.get('city')
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id from city WHERE name = \"%s\"" %(city))
	cityInfo = cur.fetchone()
	cityId = cityInfo['id']
	cur.execute("SELECT id, uid, title, address, created_at FROM property WHERE id_city = \"%d\" and (enable_booking = 0 or(enable_booking = 1 and can_book = 0))" %(cityId))
	cityProps = cur.fetchall()
	cur.execute("SELECT id_property,created_at FROM message")
	allMessages = cur.fetchall()
	propCreateMap = {}
	for diction in allMessages:
		propId = diction['id_property']
		if propId in propCreateMap:
			x = 0
		else:
			created = diction['created_at']
			propCreateMap[propId] = created
	numDays = []
	userDetails = []
	for diction in cityProps:
		pId = diction['id']
		if pId not in propCreateMap:
			days = "not Yet"
			numDays.append(days)
		else:
			listingPutUp = diction['created_at']
			firstMessage = propCreateMap[pId]
			putUpDt = datetime.datetime.fromtimestamp(listingPutUp)
			firstMessDt = datetime.datetime.fromtimestamp(firstMessage)
			elapsed = firstMessDt - putUpDt
			numDays.append(elapsed)
		uId = diction['uid']
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uId))
		temp = cur.fetchone()
		userDetails.append(temp)
	what = "firstContact"
	options = {
	"propDetails":cityProps,
	"userDetails":userDetails,
	"numDays":numDays,
	"what":what
	}
	return render_template("new.html", **options)


@routes.route('/firstContactBookNow')
def firstContactBookNow():
	city = request.args.get('city')
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id FROM city WHERE name = \"%s\"" %(city))
	cityInfo = cur.fetchone()
	cityId = cityInfo['id']
	cur.execute("SELECT id, uid, title, address, created_at FROM property WHERE id_city = \"%d\" and (enable_booking = 1 and can_book = 1)" %(cityId))
	cityProps = cur.fetchall()
	cur.execute("SELECT id_property, created_at FROM message")
	allMessages = cur.fetchall()
	propCreateMap = {}
	for diction in allMessages:
		propId = diction['id_property']
		if propId in propCreateMap:
			x = 0
		else:
			created = diction['created_at']
			propCreateMap[propId] = created
	cur.execute("SELECT bid, created_at FROM booking_queries")
	allMessages = cur.fetchall()
	for message in allMessages:
		bid = message['bid']
		cur.execute("SELECT pid FROM bookings WHERE id = \"%d\"" %(bid))
		result = cur.fetchone()
		pId = result['pid']
		if pId in propCreateMap:
			if message['created_at'] < propCreateMap[pId]:
				propCreateMap[pId] = message['created_at']
		else:
			propCreateMap[pId] = message['created_at']
	numDays = []
	userDetails = []
	for diction in cityProps:
		pId = diction['id']
		if pId not in propCreateMap:
			days = "not Yet"
			numDays.append(days)
		else:
			listingPutUp = diction['created_at']
			firstMessage = propCreateMap[pId]
			putUpDt = datetime.datetime.fromtimestamp(listingPutUp)
			firstMessDt = datetime.datetime.fromtimestamp(firstMessage)
			elapsed = firstMessDt - putUpDt
			numDays.append(elapsed)
		uId = diction['uid']
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uId))
		temp = cur.fetchone()
		userDetails.append(temp)
	what = "firstContactBookNow"
	options = {
	"propDetails":cityProps,
	"userDetails":userDetails,
	"numDays":numDays,
	"what":what
	}
	return render_template("new.html", **options)





@routes.route('/daysForClosure')
def numDaysClosure():
	city = request.args.get('city')
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id FROM city WHERE name = \"%s\"" %(city))
	cityInfo = cur.fetchone()
	cityId = cityInfo['id']
	cur.execute("SELECT id, uid, title, address, created_at FROM property WHERE id_city = \"%d\"" %(cityId))
	cityProps = cur.fetchall()
	props = []
	userDetails = []
	numDays = []
	byUs = []
	for diction in cityProps:
		pId = diction['id']
		cur.execute("SELECT * FROM filled_notification WHERE pid = \"%d\"" %(pId))
		result = cur.fetchone()
		if not result:
			x = 0
		else:
			temp = {}
			temp['uid'] = diction['uid']
			uId = diction['uid']
			temp['title'] = diction['title']
			temp['address'] = diction['address']
			temp['created_at'] = diction['created_at']
			props.append(temp)
			cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uId))
			userDet = cur.fetchone()
			userDetails.append(userDet)
			putUp = diction['created_at']
			filledUp = result['added_at']
			putUpDt = datetime.datetime.fromtimestamp(putUp)
			filledUpDt = datetime.datetime.fromtimestamp(filledUp)
			timeElapsed = filledUpDt-putUpDt
			numDays.append(timeElapsed)
			cur.execute("SELECT filled_type FROM property WHERE id = \"%d\"" %(pId))
			filledDet = cur.fetchone()
			value = filledDet['filled_type']
			if value == 1:
				temp = "yes"
				byUs.append(temp)
			elif value == 2:
				temp = "no"
				byUs.append(temp)
	what = "closure"
	options = {
	"propDetails":props,
	"userDetails":userDetails,
	"closuredays":numDays,
	"byUs":byUs,
	"what":what
	}
	return render_template("new.html", **options)


@routes.route('/subFull')
def numFullSubApartments():
	city = request.args.get('city')
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id FROM city WHERE name = \"%s\"" %(city))
	cityInfo = cur.fetchone()
	cityId = cityInfo['id']
	category = []
	propDetails = []
	userDetails = []
	cur.execute("SELECT id, uid, title, address, total_rooms, rooms FROM property WHERE id_city = \"%d\"" %(cityId))
	cityProps = cur.fetchall()
	for prop in cityProps:
		totalRooms = prop['total_rooms']
		rooms = prop['rooms']
		if  rooms == totalRooms:
			category.append("full")
		else:
			category.append("sub")
		temp = {}
		temp['id'] = prop['id']
		temp['title'] = prop['title']
		temp['address'] = prop['address']
		propDetails.append(temp)
		uId = prop['uid']
		cur.execute("SELECT first_name, last_name, email, mobile FROM landlord WHERE id = \"%d\"" %(uId))
		userDet = cur.fetchone()
		userDetails.append(userDet)
	what = "fullSub"

	options = {
	"category":category,
	"userDetails":userDetails,
	"propDetails":propDetails,
	"what":what
	}
	return render_template("new.html", **options)

@routes.route('/zipListingsContacted')
def zipListingsContacted():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id FROM zone WHERE id_city = 1 or id_city = 2 or id_city = 5")
	allZones = cur.fetchall()
	zoneIds = []
	for zone in allZones:
		zoneId = zone['id']
		zoneIds.append(zoneId)
	allZoneZipIds = []
	for zoneId in zoneIds:
		cur.execute("SELECT id_pincode FROM zone_bridge WHERE id_zone = \"%d\"" %(zoneId))
		allZoneZips = cur.fetchall()
		for zipId in allZoneZips:
			currZipId = zipId['id_pincode']
			allZoneZipIds.append(currZipId)
	totalPropsInZip = {}
	for zipId in allZoneZipIds:
		totalPropsInZip[zipId] = 0
	cur.execute("SELECT * FROM property")
	allProps = cur.fetchall()
	for prop in allProps:
		pin = prop['pin_code']
		if pin in totalPropsInZip:
			totalPropsInZip[pin] += 1
	cur.execute("SELECT * FROM message")
	zipCount = {}
	for zipId in allZoneZipIds:
		zipCount[zipId] = 0
	allMessages = cur.fetchall()
	propsSeen = {}
	for message in allMessages:
		propId = message['id_property']
		if propId in propsSeen:
			x = 0
		else:
			propsSeen[propId] = "yes"
			cur.execute("SELECT pin_code FROM property WHERE id = \"%d\"" %(propId))
			pinDet = cur.fetchone()
			pin = pinDet['pin_code']
			if pin in zipCount:
				zipCount[pin] += 1
	cur.execute("SELECT * FROM booking_queries")
	allMessages = cur.fetchall()
	for message in allMessages:
		bId = message['bid']
		cur.execute("SELECT pid FROM bookings WHERE id = \"%d\"" %(bId))
		pidDet = cur.fetchone()
		pId = pidDet['pid']
		if pId in propsSeen:
			x = 0
		else:
			propsSeen[pId] = "yes"
			cur.execute("SELECT pin_code FROM property WHERE id = \"%d\"" %(pId))
			pinDet = cur.fetchone()
			pin = pinDet['pin_code']
			if pin in zipCount:
				zipCount[pin] += 1
	propsFilledByZip = {}
	for zipId in allZoneZipIds:
		propsFilledByZip[zipId] = 0
	for key, val in propsSeen:
		pId = key
		cur.execute("SELECT filled_type FROM property WHERE id = \"%d\"" %(pId))
		typeDet = cur.fetchone()
		typez = typeDet['filled_type']
		if typez == 1 or typez == 2:
			cur.execute("SELECT pin_code FROM PROPERTY WHERE id = \"%d\"" %(pId))
			pinDet = cur.fetchone()
			pin = pinDet['pin_code']
			if pin in propsFilledByZip:
				propsFilledByZip[pin] += 1

	what = "zipListingsContacted"
	options = {
	"zipContact":zipCount,
	"zipTotalProps":totalPropsInZip,
	"zipPropsFilled":propsFilledByZip,
	"what":what
	}
	return render_template("new.html", **options)


@routes.route('/pricing')
def pricing():
	db = connect_to_database()
	cur = db.cursor()
	cur.execute("SELECT id FROM zone WHERE id_city = 1 or id_city = 2 or id_city = 5")
	allZones = cur.fetchall()
	zoneIds = []
	for zone in allZones:
		zoneId = zone['id']
		zoneIds.append(zoneId)
	allZoneZipIds = []
	for zoneId in zoneIds:
		cur.execute("SELECT id_pincode FROM zone_bridge WHERE id_zone = \"%d\"" %(zoneId))
		allZoneZips = cur.fetchall()
		for zipId in allZoneZips:
			currZipId = zipId['id_pincode']
			allZoneZipIds.append(currZipId)
	totalPropsInZip = {}
	totalFullProps = {}
	totalSubProps = {}
	zipPriceSumAll = {}
	zipPriceSumFull = {}
	zipPriceSumSub = {}
	for zipId in allZoneZipIds:
		totalFullProps[zipId] = 0
		totalSubProps[zipId] = 0
		zipPriceSumAll[zipId] = 0
		zipPriceSumFull[zipId] = 0
		zipPriceSumSub[zipId] = 0
		totalPropsInZip[zipId] = 0
	cur.execute("SELECT * FROM property")
	allProps = cur.fetchall()
	for prop in allProps:
		totalRooms = prop['total_rooms']
		rooms = prop['rooms']
		pin = prop['pin_code']
		totPrice = prop['rent']
		pricePerRoom = totPrice/prop['rooms']
		if pin in totalPropsInZip:
			totalPropsInZip[pin] += 1
			zipPriceSumAll[pin] += pricePerRoom
			if rooms == totalRooms:
				totalFullProps[pin] += 1
				zipPriceSumFull[pin] += pricePerRoom
			else:
				totalSubProps[pin] += 1
				zipPriceSumSub[pin] += pricePerRoom
	avgPriceAll = {}
	avgPriceFull = {}
	avgPriceSub = {}
	for zipId, val in totalPropsInZip:
		avgPriceAll[zipId] = zipPriceSumAll / val
	for zipId, val in totalFullProps:
		avgPriceFull[zipId] = zipPriceSumFull / val
	for zipId, val in totalSubProps:
		avgPriceSub[zipId] = zipPriceSumSub / val

	what = "pricing"

	options = {
	"avgPriceFull": avgPriceFull,
	"avgPriceSub": avgPriceSub,
	"avgPriceAll": avgPriceAll
	}

	return render_template("new.html", **options)



































	





























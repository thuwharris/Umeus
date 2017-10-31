import umeus
from umeus import models, db
from umeus.models import User, BlogPost, BlogComment
from datetime import datetime
import time

#### USERS ####
user1 = User(
		username = 'user1',
		email = 'user1@website.com',
		password = 'user1',
		authenticated = True
	)
user2 = User(
		username = 'user2',
		email = 'user2@website.com',
		password = 'user2',
		authenticated = True
	)
user3 = User(
		username = 'user3',
		email = 'user3@website.com',
		password = 'user3',
		authenticated = True
	)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.commit()


#### POSTS ####
post_format = '%d %B %Y'

post1 = BlogPost (
		datetime = datetime.strptime('14 March 2016', post_format),
		author = 'Test Author 1',
		title = 'Test Post 1',
		post = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam faucibus in tortor sodales placerat. Fusce finibus viverra leo. Pellentesque finibus libero sem. Fusce convallis dolor at turpis consectetur mollis. Nam at turpis neque. Nunc consectetur nibh id nisl maximus, quis tincidunt metus imperdiet. Phasellus mi lectus, condimentum quis tempus eget, suscipit ac ante. Pellentesque scelerisque tincidunt turpis id maximus. Suspendisse potenti.
				  Morbi id eleifend arcu. Suspendisse interdum dui ut tempus porttitor. Pellentesque molestie dui augue, ac varius lorem consequat in. Phasellus bibendum vitae elit laoreet faucibus. Nam varius mauris nec mi pellentesque aliquam. Etiam mollis consectetur ligula, id facilisis dolor luctus at. Donec aliquam sagittis vulputate. Nulla quis semper dui. Cras id sodales nulla, eget lobortis arcu. Aenean dictum congue metus ut posuere. Nulla tempus nunc id convallis scelerisque.
				  Vestibulum venenatis, lorem sed dapibus scelerisque, magna ante malesuada orci, nec accumsan mi risus ut neque. Suspendisse ut arcu justo. Cras viverra sem id ipsum fringilla finibus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam mollis risus nunc, id placerat neque tincidunt at. Nullam at convallis ipsum. Morbi turpis ante, pharetra vel volutpat id, ultrices ut sem. Quisque blandit varius justo id accumsan. Nunc eu luctus lectus, tincidunt posuere dui. Etiam suscipit turpis vel finibus dictum. In egestas orci nisl, ac sagittis ex iaculis eget. Fusce placerat massa augue, quis porta diam mattis sed.''',
		tags = '|tag1|tag2|tag3|'
	)

post2 = BlogPost (
		datetime = datetime.strptime('05 May 2016', post_format),
		author = 'Test Author 2',
		title = 'Test Post 2',
		post = 'Proin at lectus vestibulum, feugiat tellus sit amet, commodo leo. Sed nec tempus augue. Nunc enim urna, porta in semper sed, fermentum nec nibh. Phasellus rhoncus porta convallis. Pellentesque laoreet dictum diam, in placerat leo euismod non. Maecenas ullamcorper tortor pretium, interdum tortor a, tincidunt metus. Aliquam vitae dolor id nisi tincidunt rhoncus ut a massa. Nunc imperdiet gravida enim posuere hendrerit. Morbi vel nisl id est euismod iaculis. Duis sed enim vitae erat molestie placerat sed eu dolor. Phasellus lacus tellus, efficitur sit amet quam quis, vehicula posuere tellus. Cras vehicula purus nisl, at pretium nunc congue quis. Nulla interdum placerat elit nec commodo. Nulla blandit tristique diam, a faucibus ipsum congue efficitur. Vivamus condimentum sagittis leo, quis tincidunt dolor lacinia sed.',
		tags = '|tag2|tag4|'
	)

post3 = BlogPost (
		datetime = datetime.now(),
		author = 'Test Author 3',
		title = 'Test Post 3',
		post = '''Nam facilisis eros in mauris eleifend fringilla. Mauris at vestibulum nibh, at ornare augue. Fusce erat nulla, commodo a dolor eu, luctus gravida ante. Aliquam euismod est quis orci dignissim rutrum. Donec pellentesque, nunc ac dapibus auctor, metus enim vestibulum turpis, eget condimentum turpis nunc in enim. Aliquam blandit justo magna, non condimentum sem sodales a. Ut viverra sed eros nec euismod. Vestibulum ac tellus rutrum, consequat orci ut, ullamcorper turpis.
				  Curabitur vitae felis eget risus cursus suscipit. Quisque eu posuere urna. Nullam ac nisl consectetur, pretium orci vel, aliquet arcu. Fusce mattis, est eu fermentum finibus, metus tellus feugiat enim, non aliquet erat dolor sit amet purus. Fusce quis finibus odio. Proin semper erat iaculis pellentesque blandit. Donec hendrerit congue magna, at iaculis felis fermentum id. Donec tempor et elit ut vulputate.
				  Fusce efficitur magna vitae massa mollis, quis posuere massa luctus. Fusce finibus, erat id posuere accumsan, nisi eros maximus est, sed aliquet neque enim eget ipsum. In hac habitasse platea dictumst. Aliquam erat volutpat. Morbi eu consectetur nulla. Integer condimentum turpis quis neque dignissim, eget volutpat justo vestibulum. Aliquam imperdiet nibh turpis. Sed sit amet sollicitudin arcu. Suspendisse potenti. Fusce varius risus arcu, in elementum ante commodo in. Ut dapibus convallis nisi nec pellentesque. Etiam mattis lacus sed justo consectetur congue. Sed posuere scelerisque mi. Nam lacinia lacinia nisl, a varius magna. Mauris arcu tellus, tristique vitae luctus eu, euismod consectetur mauris. Nam lacinia bibendum risus eget laoreet. ''',
		tags = '|tag3|'
	)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()

### COMMENTS ###

comment_format = '%I:%M:%S %p GMT on %d/%m/%y'

comment1 = BlogComment (
			datetime = datetime.strptime('01:02:03 am GMT on 15/03/16', comment_format),
			user_id = user1.user_id,
			post_id = post1.post_id,
			comment = 'Test comment 1 on post 1 by user 1'
		)
comment2 = BlogComment (
			datetime = datetime.strptime('01:04:12 am GMT on 15/03/16', comment_format),
			user_id = user2.user_id,
			post_id = post1.post_id,
			comment = 'Test comment 2 on post 1 by user 2'
		)
comment3 = BlogComment (
			datetime = datetime.strptime('02:19:11 pm GMT on 17/04/16', comment_format),
			user_id = user3.user_id,
			post_id = post1.post_id,
			comment = 'Test comment 3 on post 1 by user 3'
		)

comment4 = BlogComment (
			datetime = datetime.strptime('09:11:11 am GMT on 20/05/16', comment_format),
			user_id = user2.user_id,
			post_id = post2.post_id,
			comment = 'Test comment on post 2 by user 2'
		)

comment5 = BlogComment (
			datetime = datetime.strptime('12:15:01 am GMT on 15/03/16', comment_format),
			user_id = user2.user_id,
			post_id = post3.post_id,
			comment = 'Test comment 1 on post 3 by user 2'
		)
comment6 = BlogComment (
			datetime = datetime.strptime('10:14:01 pm GMT on 15/03/16', comment_format),
			user_id = user3.user_id,
			post_id = post3.post_id,
			comment = 'Test comment 2 on post 3 by user 3'
		)

db.session.add(comment1)
db.session.add(comment2)
db.session.add(comment3)
db.session.add(comment4)
db.session.add(comment5)
db.session.add(comment6)
db.session.commit()

########################

for i in range(0,50):
	comment = BlogComment(
		user_id = user1.user_id,
		post_id = post3.post_id,
		datetime = datetime.now(),
		comment = 'Test Comment ' + str(i)
	)

	db.session.add(comment)

db.session.commit()

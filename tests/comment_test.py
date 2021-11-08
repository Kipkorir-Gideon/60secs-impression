from app.models import Comments, User
from app import db

def setUp(self):
  self.new_user = User(username = 'Gidalios',password = 'gideon.', email = 'gidalios@gmail.com')
  self.new_comment = Comments(id=3,user_id=5,comment='That is awesome', pitch_id = 3 )

def tearDown(self):
  Comments.query.delete()
  User.query.delete()
        
def test_check_instance_variables(self):
  self.assertEquals(self.new_comment.id,3)
  self.assertEquals(self.new_comment.user_id,5)
  self.assertEquals(self.new_comment.comment,'Awesome pitch')
  self.assertEquals(self.new_comment.pitch_id,3)
        
def test_save_comment(self):
  self.new_comment.save_comment()
  self.assertTrue(len(Comments.query.all())>0)
        
def test_get_comment_by_id(self):
  self.new_comment.save_comment()
  got_comments = Comments.get_comments(3)
  self.assertTrue(len(got_comments) == 1)
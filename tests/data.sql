INSERT INTO user (username, password) 
VALUES
    ('testUser',X'24326224313224463246326d3938584a6b796f7759476d3245796c4675336c684d2f3462696830544e50467351504e595242716455447865412f5143'),
    ('userTwo',X'24326224313224594d65437334526a4b69726e4f786f65446e4d3130654c5270455065436938784d6f34303078542e665375454c736d3778354f342e');

-- Data:
-- 1. Username: testUser
--    Password: usertest
-- 2. Username: userTwo
--    Password: twouser

INSERT INTO images (user_id, img_path, img_name) 
VALUES
(1,'/uploads/burger.jpg','burger.jpg'),
(1,'/uploads/football.jpg','football.jpg'),
(2,'/uploads/kitchen.jpg','kitchen.jpg');
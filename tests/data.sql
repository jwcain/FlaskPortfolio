INSERT INTO user (username, password)
VALUES
    ('admintest', 'pbkdf2:sha256:600000$5vVJL77wWCNXHZzI$891572b56d661c3980ec96c95a18a0818b7339046815e9dfaf9aee38d505cc4b');


INSERT INTO recipe (title, info)
VALUES
    ('Water Soup', 'Water soup, can be chilled for hot days!'),
    ('Broth Soup', 'A step up in Culinary prefection!');

INSERT INTO recipe_step (recipe_id, step_id, info)
VALUES
    (1, 1, 'Collect a Bowl'),
    (1, 2, 'Fill it with water'),
    (1, 3, 'Optional: Add Ice'),
    (1, 1, 'Collect a Bowl'),
    (1, 2, 'Fill it with broth');

INSERT INTO recipe_ingredient (recipe_id, step_id, amount, ingredient_name)
VALUES
    (1, 1, '1', 'Bowl'),
    (1, 2, 'Bowlfull', 'Water'),
    (1, 3, 'Handfull', 'Ice'),
    (2, 1, '1', 'Bowl'),
    (2, 2, 'Bowlfull', 'Broth');

INSERT INTO project (shown, programming_language, tools_used, title, info, link_github, link_live, last_updated)
VALUES
    (1, 'Python', 'Flask','Portfolio Website','Portfolio to show off my skills','githublink/index', '', '2023-08-01 00:00:00'),
    (1, 'C#','Unity', 'Hexquisite', 'A hexagonal block puzzle game.','githublink/hexquisite', 'hex.play/live', '2023-08-01 05:00:55'),
    (0, 'Java','', 'Java Tutorial Project', 'stadnard java tutorial','', '', '2017-08-01 05:00:55');

INSERT INTO work_experience (shown, title, one_liner, dates, work_location)
VALUES
    (1,'Python Developer', 'Developed a flask-based website','July 23 - Aug-23', 'Home'),
    (0,'Baker', 'Baked the best peanut butter cookies','Everyday', 'Everywhere');

INSERT INTO work_experience_point (work_experience_id, info)
VALUES
    (1,'Learned Flask'),
    (1,'Converted Portfolio'),
    (1,'Webdev is fun!'),
    (0,'Made way too many cookies'),
    (0,'I am also good at cheesecake');
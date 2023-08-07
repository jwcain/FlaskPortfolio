INSERT INTO user (username, password)
VALUES
    ('admin', 'pbkdf2:sha256:600000$5vVJL77wWCNXHZzI$891572b56d661c3980ec96c95a18a0818b7339046815e9dfaf9aee38d505cc4b');


INSERT INTO recipe (title, summary, info)
VALUES
    ('Water Soup', 'Water soup, can be chilled for hot days!', 'Water soup, can be chilled for hot days!'),
    ('Broth Soup', 'A step up in Culinary prefection!', 'A step up in Culinary prefection!');

INSERT INTO recipe_step (recipe_id, step_order, info)
VALUES
    (1, 1, 'Collect a Bowl'),
    (1, 2, 'Fill it with water'),
    (1, 3, 'Optional: Add Ice'),
    (2, 1, 'Collect a Bowl'),
    (2, 2, 'Fill it with broth');

INSERT INTO recipe_ingredient (recipe_id, step_id, amount, ingredient_name)
VALUES
    (1, 1, '1', 'Bowl'),
    (1, 2, 'Bowlfull', 'Water'),
    (1, 3, 'Handfull', 'Ice'),
    (2, 1, '1', 'Bowl'),
    (2, 2, 'Bowlfull', 'Broth');

INSERT INTO project (shown, programming_language, tools_used, title, info, last_updated)
VALUES
    (1, 'Python', 'Flask','Portfolio Website','Portfolio to show off my skills', '2023-08-01'),
    (1, 'C#','Unity', 'Hexquisite', 'A hexagonal block puzzle game.', '2023-08-01'),
    (0, 'Java','', 'Java Tutorial Project', 'stadnard java tutorial', '2017-08-01');

INSERT INTO project_link (project_id, title, link) 
VALUES
    (1, 'Github', '/index' ),
    (2, 'Github', '/index'),
    (2, 'Play Now', '/index');
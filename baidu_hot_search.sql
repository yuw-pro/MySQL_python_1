USE baidu_hot_search_sql;

CREATE TABLE IF NOT EXISTS hot_search (
    id INT PRIMARY KEY AUTO_INCREMENT,
    rank_no INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    hot_value VARCHAR(50),
    url VARCHAR(500),
    fetched_time DATETIME
);

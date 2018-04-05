CREATE SCHEMA IF NOT EXISTS `eslinthub` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `eslinthub`.`ut_repos` (
  `repo_id` INT NOT NULL,
  `repo_name` VARCHAR(45) NULL,
  `html_url` VARCHAR(128) NULL,
  `ESlint` VARCHAR(1) NULL,
  `insert_dttm` DATETIME NOT NULL,
  `last_modified` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`repo_id`),
  INDEX `name` (`repo_name` ASC),
  INDEX `html_url` (`html_url` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `eslinthub`.`ut_eslint_issues` (
  `eslint_issues_id` INT NOT NULL,
  `repo_id` INT NOT NULL,
  `issue_description` VARCHAR(4096) NOT NULL,
  `file_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`eslint_issues_id`),
  INDEX `fk_ut_eslint_issues_1_idx` (`repo_id` ASC),
  CONSTRAINT `fk_ut_eslint_issues_1`
    FOREIGN KEY (`repo_id`)
    REFERENCES `eslinthub`.`ut_repos` (`repo_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
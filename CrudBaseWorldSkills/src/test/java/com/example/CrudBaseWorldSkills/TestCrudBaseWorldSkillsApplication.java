package com.example.CrudBaseWorldSkills;

import org.springframework.boot.SpringApplication;

public class TestCrudBaseWorldSkillsApplication {

	public static void main(String[] args) {
		SpringApplication.from(CrudBaseWorldSkillsApplication::main).with(TestcontainersConfiguration.class).run(args);
	}

}

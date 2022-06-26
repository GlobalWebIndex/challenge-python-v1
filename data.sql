INSERT INTO public.auth_group (id, "name") VALUES(1, 'Developer Members');
INSERT INTO public.auth_group (id, "name") VALUES(2, 'Administrator Members');

INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES(1, 'pbkdf2_sha256$260000$TSplXe0X7F5TocuxAEzhqn$B2T24sTiSrYr4chv5tX+f89QGxNMXlNKW4l0dwic6mc=', '2022-06-26 18:15:47.184', true, 'alex', '', '', 'alex@alex.com', true, true, '2022-06-19 17:52:12.694');
INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES(2, 'pbkdf2_sha256$260000$f49VASYEae6NhscSHX0Z41$MMFqFLWt4w6NPYD7uBPzVnCcSZTbAuvt0VGV4umhoGM=', '2022-06-26 18:18:14.631', false, 'admin', '', '', '', false, true, '2022-06-19 18:04:56.000');
INSERT INTO public.auth_user (id, "password", last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES(3, 'pbkdf2_sha256$260000$8LFN5ob61jjbepPwXbdaOJ$ubql1wEmfsQeOUmhH9xMSwo9pRAc8QtcVyqKiSvZhNc=', '2022-06-26 18:17:20.665', false, 'developer', '', '', '', false, true, '2022-06-19 18:05:19.000');

-- INSERT INTO public.auth_permission (id, "name", content_type_id, codename) VALUES(29, 'User can create/edit/delete dinosaurs', 7, 'can_edit');

INSERT INTO public.auth_group_permissions (id, group_id, permission_id) VALUES(2, 2, 29);

INSERT INTO public.auth_user_groups (id, user_id, group_id) VALUES(1, 2, 2);
INSERT INTO public.auth_user_groups (id, user_id, group_id) VALUES(2, 3, 1);

INSERT INTO public.dinosaurs_dinosaur (id, "name", eating_classification, colour, "period", "size", image_1, image_2) VALUES
     (1, 'Tyrannosaurus Rex', 'carnivore', 'Brown', 'jurassic', 'large', 'Jurassic_Park_Tyrannosaurus_Rex_DeFq0VT.webp', 'Tyrannosaurus-rex.jpg'),
     (2, 'Therizinosaurus','herbivore','Grey','jurassic','medium','Therizinosaurus_Zazzle_DGAdhfi.webp',''),
	 (3, 'Velociraptor','carnivore','Grey','cretaceous','small','Velociraptor-info-graphic_Ou8rDHm.webp','unnamed.png'),
	 (4, 'Giganotosaurus','herbivore','Green','cretaceous','very large','Giganotasaurus_Jurassic_World_Dominion_Ffr9P6K.webp',''),
	 (5, 'Spinosaurus','carnivore','Grey','paleogene','small','Spinoboi_YrNmM9M.webp','istock-146818770.jpg'),
	 (6, 'Triceratops','carnivore','Brown','cretaceous','large','triceratops.webp',''),
	 (7, 'Stegosaurus','carnivore','Brown','cretaceous','medium','Stegosaurus.webp',''),
	 (8, 'Archaeopteryx','carnivore','Brown','cretaceous','small','archaeoptery.webp',''),
	 (9, 'Brachiosaurus','carnivore','Green','cretaceous','very large','brachiosaurus.webp',''),
	 (10, 'Allosaurus','carnivore','Brown','cretaceous','medium','allosaurus.webp',''),
     (11, 'Dracorex','carnivore','Green','neogene','medium','dracorex.jpg',''),
	 (12, 'Dilophosaurus','carnivore','Brown','cretaceous','small','Dilophosaurus_Render.webp',''),
	 (13, 'Iguanodon','carnivore','Brown','cretaceous','medium','iguanodon-1_e1e9.jpg','');




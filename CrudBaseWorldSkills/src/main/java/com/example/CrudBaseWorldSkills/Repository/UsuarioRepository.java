package com.example.CrudBaseWorldSkills.Repository;

import com.example.CrudBaseWorldSkills.Model.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
}

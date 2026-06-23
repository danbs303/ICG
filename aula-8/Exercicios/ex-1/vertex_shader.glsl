#version 330 core

// Atributos de entrada
layout (location = 0) in vec2 aPos;      // Posição 2D
layout (location = 1) in vec3 aNormal;   // Normal

// Saídas para o Fragment Shader
out vec3 FragPos;
out vec3 Normal;

void main()
{
    // A posição em 3D (z = 0)
    vec3 pos3D = vec3(aPos, 0.0);
    
    // Envia para o Fragment Shader
    FragPos = pos3D;
    Normal = aNormal;
    
    // Posição final (projeção ortográfica simples)
    gl_Position = vec4(aPos, 0.0, 1.0);
}
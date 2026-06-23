#version 330 core

layout (location = 0) in vec2 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 FragPos;
out vec3 Normal;

void main()
{
    vec3 pos3D = vec3(aPos, 0.0);
    FragPos = pos3D;
    Normal = aNormal;
    gl_Position = vec4(aPos, 0.0, 1.0);
}
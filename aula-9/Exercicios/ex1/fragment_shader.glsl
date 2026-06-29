#version 330 core

in vec2 TexCoord;

uniform sampler2D uTexture;

out vec4 FragColor;

void main()
{
    // Aplica a textura com as coordenadas UV (0 a 3)
    // GL_REPEAT faz com que a textura se repita automaticamente
    FragColor = texture(uTexture, TexCoord);
}
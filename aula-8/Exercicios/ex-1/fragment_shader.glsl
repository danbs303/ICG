#version 330 core

// Entradas do Vertex Shader
in vec3 FragPos;
in vec3 Normal;

// Uniforms
uniform vec3 uLightPos;
uniform vec3 uViewPos;
uniform float uTime;

// Saída
out vec4 FragColor;

void main()
{
    // --- CORES ---
    vec3 objectColor = vec3(0.3, 0.6, 0.9);  // Azul claro
    vec3 lightColor = vec3(1.0, 1.0, 1.0);   // Branco
    vec3 alertColor = vec3(1.0, 0.0, 0.0);   // Vermelho
    
    // --- ILUMINAÇÃO AMBIENTE ---
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;
    
    // --- ILUMINAÇÃO DIFUSA ---
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(uLightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    
    // ============================================================
    // EFEITO DE ALERTA - OSCILAÇÃO ENTRE AZUL E VERMELHO
    // ============================================================
    // Oscila entre 0 e 1 usando seno
    float pulse = (sin(uTime * 2.0) + 1.0) / 2.0;
    
    // A cor da luz difusa oscila entre a cor original e vermelho
    vec3 diffuseColor = mix(lightColor, alertColor, pulse);
    
    // Aplica a intensidade difusa
    vec3 diffuse = diff * diffuseColor;
    
    // --- ILUMINAÇÃO ESPECULAR (básica) ---
    float specularStrength = 0.5;
    vec3 viewDir = normalize(uViewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;
    
    // --- COMPONENTE EXTRA: Brilho pulsante ---
    float glow = 0.3 * pulse;
    vec3 emission = glow * alertColor;
    
    // --- RESULTADO FINAL ---
    vec3 result = (ambient + diffuse + specular + emission) * objectColor;
    
    // Saída
    FragColor = vec4(result, 1.0);
}
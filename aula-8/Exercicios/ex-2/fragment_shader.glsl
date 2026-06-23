#version 330 core

in vec3 FragPos;
in vec3 Normal;

uniform vec3 uLightPos;
uniform vec3 uViewPos;

// ============================================================
// UNIFORM PARA O EXERCÍCIO 2: CONTROLE DO SHININESS
// ============================================================
uniform float uShininess;  // Enviado pelo Python via teclado

out vec4 FragColor;

void main()
{
    // --- CORES ---
    vec3 objectColor = vec3(0.3, 0.6, 0.9);  // Azul
    vec3 lightColor = vec3(1.0, 1.0, 1.0);   // Branco
    
    // --- ILUMINAÇÃO AMBIENTE ---
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * lightColor;
    
    // --- ILUMINAÇÃO DIFUSA ---
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(uLightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    // ============================================================
    // EXERCÍCIO 2: CÁLCULO ESPECULAR COM SHININESS DINÂMICO
    // ============================================================
    float specularStrength = 0.6;
    vec3 viewDir = normalize(uViewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    
    // ============================================================
    // O VALOR DE uShininess É CONTROLADO PELO TECLADO EM PYTHON
    // Valores baixos (ex: 2.0)  -> material fosco (brilho espalhado)
    // Valores altos (ex: 128.0) -> material polido (brilho concentrado)
    // ============================================================
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), uShininess);
    vec3 specular = specularStrength * spec * lightColor;
    
    // --- RESULTADO FINAL ---
    vec3 result = (ambient + diffuse + specular) * objectColor;
    
    FragColor = vec4(result, 1.0);
}
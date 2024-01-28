#version 430 core

out vec2 tex_coord;

void main()
{
    switch (gl_VertexID)
    {
        case 0:
        case 5:
        {
            gl_Position = vec4(-1, -1, 0.0, 1.0); 
            tex_coord = vec2(0, 0);
            break;
        }

        case 1:
        {
            gl_Position = vec4(1, -1, 0.0, 1.0); 
            tex_coord = vec2(1, 0);
            break;
        }

        case 2:
        case 3:
        {
            gl_Position = vec4(1, 1, 0.0, 1.0); 
            tex_coord = vec2(1, 1);
            break;
        }

        case 4:
        {
            gl_Position = vec4(-1, 1, 0.0, 1.0); 
            tex_coord = vec2(0, 1);
            break;
        }
    }
}
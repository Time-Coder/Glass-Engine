#version 460 core

in flat int visible;

void main()
{
    if (visible == 0)
    {
        discard;
    }
}
void arnold_image(
    sampler2D tex_sampler,
    int filtertype,
    int mipmap_bias,
    vec3 multiply,
    vec3 offset,
    int color_space,
    bool ignore_missing_textures,
    vec4 missing_texture_color,
    int uvset,
    vec2 uvcoords,
    float soffset,
    float toffset,
    int swrap,
    int twrap,
    float sscale,
    float tscale,
    bool sflip,
    bool tflip,
    bool swap_st,
    bool single_channel,
    int start_channel,
    out vec4 result)
{
    vec2 uv = vec2((uvcoords.x + soffset), (uvcoords.y + toffset));
    if (swap_st)
    {
        uv = vec2(uv.y, uv.x);
    }
    if (sflip)
    {
        uv.x = 1.0 - uv.x;
    }
    if (tflip)
    {
        uv.y = 1.0 - uv.y;
    }
    uv = vec2(sscale * uv.x, 1.0 - tscale * uv.y);

    vec4 lookup = texture(tex_sampler, uv);
    if (start_channel == 1)
    {
        lookup = lookup.gbaa;
    }
    else if (start_channel == 2)
    {
        lookup = lookup.baaa;
    }
    else if (start_channel == 3)
    {
        lookup = lookup.aaaa;
    }
    
    if (single_channel)
    {
        lookup = vec4(lookup.rrr, 1.0);
    }
    
    result = vec4(multiply * lookup.rgb + offset, lookup.a);
}

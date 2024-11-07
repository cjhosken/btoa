#include "lib/arnold_image.glsl"

void arnold_image_color3(
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
    out vec3 result)
{
    vec4 lookup;
    arnold_image(
        tex_sampler,
        filtertype,
        mipmap_bias,
        multiply,
        offset,
        color_space,
        ignore_missing_textures,
        missing_texture_color,
        uvset,
        uvcoords,
        soffset,
        toffset,
        swrap,
        twrap,
        sscale,
        tscale,
        sflip,
        tflip,
        swap_st,
        single_channel,
        start_channel,
        lookup);

    result = lookup.rgb;
}

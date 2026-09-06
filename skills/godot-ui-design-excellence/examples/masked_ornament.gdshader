// Original decorative example. Documentation-reviewed; not compiled in Godot here.
// Supply a grayscale mask in the red channel, and test the installed renderer.
// Use on ornament only; native text, focus, and interaction should remain separate.
shader_type canvas_item;

uniform sampler2D reveal_mask : repeat_disable, filter_linear;
uniform float reveal : hint_range(0.0, 1.0) = 1.0;
uniform float softness : hint_range(0.001, 0.2) = 0.05;

void fragment() {
    // In a canvas_item fragment, COLOR already includes the default texture and
    // modulation in the normal path. Do not multiply the base texture twice.
    vec4 base = COLOR;
    float mask_value = clamp(texture(reveal_mask, UV).r, 0.0, 1.0);
    float safe_softness = max(softness, 0.001);
    float threshold = mix(-safe_softness, 1.0 + safe_softness,
                          clamp(reveal, 0.0, 1.0));
    float coverage = smoothstep(mask_value - safe_softness,
                                mask_value + safe_softness, threshold);
    COLOR = vec4(base.rgb, base.a * coverage);
}

from .ShaderSyntaxTokens import Var, Struct, Func

from OpenGL import GL


class ShaderBuiltins:
    is_resolved = False
    ins = {
        GL.GL_VERTEX_SHADER: {
            "gl_VertexID": Var(name="gl_VertexID", type="int"),
            "gl_InstanceID": Var(name="gl_InstanceID", type="int"),
            "gl_DrawID": Var(name="gl_DrawID", type="int"),
            "gl_BaseVertex": Var(name="gl_BaseVertex", type="int"),
            "gl_BaseInstance": Var(name="gl_BaseInstance", type="int"),
        },
        GL.GL_TESS_CONTROL_SHADER: {
            "gl_PatchVerticesIn": Var(name="gl_PatchVerticesIn", type="int"),
            "gl_PrimitiveID": Var(name="gl_PrimitiveID", type="int"),
            "gl_InvocationID": Var(name="gl_InvocationID", type="int"),
            "gl_in": Var(name="gl_in", type="gl_PerVertex[]"),
        },
        GL.GL_TESS_EVALUATION_SHADER: {
            "gl_TessCoord": Var(name="gl_TessCoord", type="vec3"),
            "gl_PatchVerticesIn": Var(name="gl_PatchVerticesIn", type="int"),
            "gl_PrimitiveID": Var(name="gl_PrimitiveID", type="int"),
            "gl_TessLevelOuter": Var(name="gl_TessLevelOuter", type="float[4]"),
            "gl_TessLevelInner": Var(name="gl_TessLevelInner", type="float[2]"),
            "gl_in": Var(name="gl_in", type="gl_PerVertex[]"),
        },
        GL.GL_GEOMETRY_SHADER: {
            "gl_in": Var(name="gl_in", type="gl_PerVertex[]"),
            "gl_PrimitiveIDIn": Var(name="gl_PrimitiveIDIn", type="int"),
            "gl_InvocationID": Var(name="gl_InvocationID", type="int"),
        },
        GL.GL_FRAGMENT_SHADER: {
            "gl_FragCoord": Var(name="gl_FragCoord", type="vec4"),
            "gl_FrontFacing": Var(name="gl_FrontFacing", type="bool"),
            "gl_PointCoord": Var(name="gl_PointCoord", type="vec2"),
            "gl_SampleID": Var(name="gl_SampleID", type="int"),
            "gl_SamplePosition": Var(name="gl_SamplePosition", type="vec2"),
            "gl_SampleMaskIn": Var(name="gl_SampleMaskIn", type="int[]"),
            "gl_ClipDistance": Var(name="gl_ClipDistance", type="float[]"),
            "gl_PrimitiveID": Var(name="gl_PrimitiveID", type="int"),
            "gl_Layer": Var(name="gl_Layer", type="int"),
            "gl_ViewportIndex": Var(name="gl_ViewportIndex", type="int"),
        },
        GL.GL_COMPUTE_SHADER: {
            "gl_NumWorkGroups": Var(name="gl_NumWorkGroups", type="uvec3"),
            "gl_WorkGroupID": Var(name="gl_WorkGroupID", type="uvec3"),
            "gl_LocalInvocationID": Var(name="gl_LocalInvocationID", type="uvec3"),
            "gl_GlobalInvocationID": Var(name="gl_GlobalInvocationID", type="uvec3"),
            "gl_LocalInvocationIndex": Var(name="gl_LocalInvocationIndex", type="uint"),
            "gl_WorkGroupSize": Var(name="gl_WorkGroupSize", type="uvec3"),
        },
    }

    outs = {
        GL.GL_VERTEX_SHADER: {
            "gl_Position": Var(name="gl_Position", type="vec4"),
            "gl_PointSize": Var(name="gl_PointSize", type="float"),
            "gl_ClipDistance": Var(name="gl_ClipDistance", type="float[]"),
        },
        GL.GL_TESS_CONTROL_SHADER: {
            "gl_TessLevelOuter": Var(name="gl_TessLevelOuter", type="float[4]"),
            "gl_TessLevelInner": Var(name="gl_TessLevelInner", type="float[2]"),
            "gl_out": Var(name="gl_out", type="gl_PerVertex[]"),
        },
        GL.GL_TESS_EVALUATION_SHADER: {
            "gl_Position": Var(name="gl_Position", type="vec4"),
            "gl_PointSize": Var(name="gl_PointSize", type="float"),
            "gl_ClipDistance": Var(name="gl_ClipDistance", type="float[]"),
        },
        GL.GL_GEOMETRY_SHADER: {
            "gl_Position": Var(name="gl_Position", type="vec4"),
            "gl_PointSize": Var(name="gl_PointSize", type="float"),
            "gl_ClipDistance": Var(name="gl_ClipDistance", type="float[]"),
            "gl_PrimitiveID": Var(name="gl_PrimitiveID", type="int"),
            "gl_Layer": Var(name="gl_Layer", type="int"),
            "gl_ViewportIndex": Var(name="gl_ViewportIndex", type="int"),
        },
        GL.GL_FRAGMENT_SHADER: {
            "gl_FragDepth": Var(name="gl_FragDepth", type="float"),
            "gl_SampleMask": Var(name="gl_SampleMask", type="int[]"),
        },
    }

    structs = {
        "gl_PerVertex": Struct(
            name="gl_PerVertex",
            members={
                "gl_Position": Var(name="gl_Position", type="vec4"),
                "gl_PointSize": Var(name="gl_PointSize", type="float"),
                "gl_ClipDistance": Var(name="gl_ClipDistance", type="float[]"),
            },
        ),
        "gl_DepthRangeParameters": Struct(
            name="gl_DepthRangeParameters",
            members={
                "near": Var(name="near", type="float"),
                "far": Var(name="far", type="float"),
                "diff": Var(name="diff", type="float"),
            },
        ),
    }

    uniforms = {
        "gl_DepthRange": Var(name="gl_DepthRange", type="gl_DepthRangeParameters"),
        "gl_NumSamples": Var(name="gl_NumSamples", type="int"),
    }

    global_vars = {
        "gl_MaxVertexAttribs": Var(name="gl_MaxVertexAttribs", type="int"),
        "gl_MaxVertexOutputComponents": Var(
            name="gl_MaxVertexOutputComponents", type="int"
        ),
        "gl_MaxVertexUniformComponents": Var(
            name="gl_MaxVertexUniformComponents", type="int"
        ),
        "gl_MaxVertexTextureImageUnits": Var(
            name="gl_MaxVertexTextureImageUnits", type="int"
        ),
        "gl_MaxGeometryInputComponents": Var(
            name="gl_MaxGeometryInputComponents", type="int"
        ),
        "gl_MaxGeometryOutputComponents": Var(
            name="gl_MaxGeometryOutputComponents", type="int"
        ),
        "gl_MaxGeometryUniformComponents": Var(
            name="gl_MaxGeometryUniformComponents", type="int"
        ),
        "gl_MaxGeometryTextureImageUnits": Var(
            name="gl_MaxGeometryTextureImageUnits", type="int"
        ),
        "gl_MaxGeometryOutputVertices": Var(
            name="gl_MaxGeometryOutputVertices", type="int"
        ),
        "gl_MaxGeometryTotalOutputComponents": Var(
            name="gl_MaxGeometryTotalOutputComponents", type="int"
        ),
        "gl_MaxGeometryVaryingComponents": Var(
            name="gl_MaxGeometryVaryingComponents", type="int"
        ),
        "gl_MaxFragmentInputComponents": Var(
            name="gl_MaxFragmentInputComponents", type="int"
        ),
        "gl_MaxDrawBuffers": Var(name="gl_MaxDrawBuffers", type="int"),
        "gl_MaxFragmentUniformComponents": Var(
            name="gl_MaxFragmentUniformComponents", type="int"
        ),
        "gl_MaxTextureImageUnits": Var(name="gl_MaxTextureImageUnits", type="int"),
        "gl_MaxClipDistances": Var(name="gl_MaxClipDistances", type="int"),
        "gl_MaxCombinedTextureImageUnits": Var(
            name="gl_MaxCombinedTextureImageUnits", type="int"
        ),
        "gl_MaxTessControlInputComponents": Var(
            name="gl_MaxTessControlInputComponents", type="int"
        ),
        "gl_MaxTessControlOutputComponents": Var(
            name="gl_MaxTessControlOutputComponents", type="int"
        ),
        "gl_MaxTessControlUniformComponents": Var(
            name="gl_MaxTessControlUniformComponents", type="int"
        ),
        "gl_MaxTessControlTextureImageUnits": Var(
            name="gl_MaxTessControlTextureImageUnits", type="int"
        ),
        "gl_MaxTessControlTotalOutputComponents": Var(
            name="gl_MaxTessControlTotalOutputComponents", type="int"
        ),
        "gl_MaxTessEvaluationInputComponents": Var(
            name="gl_MaxTessEvaluationInputComponents", type="int"
        ),
        "gl_MaxTessEvaluationOutputComponents": Var(
            name="gl_MaxTessEvaluationOutputComponents", type="int"
        ),
        "gl_MaxTessEvaluationUniformComponents": Var(
            name="gl_MaxTessEvaluationUniformComponents", type="int"
        ),
        "gl_MaxTessEvaluationTextureImageUnits": Var(
            name="gl_MaxTessEvaluationTextureImageUnits", type="int"
        ),
        "gl_MaxTessPatchComponents": Var(name="gl_MaxTessPatchComponents", type="int"),
        "gl_MaxPatchVertices": Var(name="gl_MaxPatchVertices", type="int"),
        "gl_MaxTessGenLevel": Var(name="gl_MaxTessGenLevel", type="int"),
        "gl_MaxViewports": Var(name="gl_MaxViewports", type="int"),
        "gl_MaxVertexUniformVectors": Var(
            name="gl_MaxVertexUniformVectors", type="int"
        ),
        "gl_MaxFragmentUniformVectors": Var(
            name="gl_MaxFragmentUniformVectors", type="int"
        ),
        "gl_MaxVaryingVectors": Var(name="gl_MaxVaryingVectors", type="int"),
        "gl_MaxVertexImageUniforms": Var(name="gl_MaxVertexImageUniforms", type="int"),
        "gl_MaxVertexAtomicCounters": Var(
            name="gl_MaxVertexAtomicCounters", type="int"
        ),
        "gl_MaxVertexAtomicCounterBuffers": Var(
            name="gl_MaxVertexAtomicCounterBuffers", type="int"
        ),
        "gl_MaxTessControlImageUniforms": Var(
            name="gl_MaxTessControlImageUniforms", type="int"
        ),
        "gl_MaxTessControlAtomicCounters": Var(
            name="gl_MaxTessControlAtomicCounters", type="int"
        ),
        "gl_MaxTessControlAtomicCounterBuffers": Var(
            name="gl_MaxTessControlAtomicCounterBuffers", type="int"
        ),
        "gl_MaxTessEvaluationImageUniforms": Var(
            name="gl_MaxTessEvaluationImageUniforms", type="int"
        ),
        "gl_MaxTessEvaluationAtomicCounters": Var(
            name="gl_MaxTessEvaluationAtomicCounters", type="int"
        ),
        "gl_MaxTessEvaluationAtomicCounterBuffers": Var(
            name="gl_MaxTessEvaluationAtomicCounterBuffers", type="int"
        ),
        "gl_MaxGeometryImageUniforms": Var(
            name="gl_MaxGeometryImageUniforms", type="int"
        ),
        "gl_MaxGeometryAtomicCounters": Var(
            name="gl_MaxGeometryAtomicCounters", type="int"
        ),
        "gl_MaxGeometryAtomicCounterBuffers": Var(
            name="gl_MaxGeometryAtomicCounterBuffers", type="int"
        ),
        "gl_MaxFragmentImageUniforms": Var(
            name="gl_MaxFragmentImageUniforms", type="int"
        ),
        "gl_MaxFragmentAtomicCounters": Var(
            name="gl_MaxFragmentAtomicCounters", type="int"
        ),
        "gl_MaxFragmentAtomicCounterBuffers": Var(
            name="gl_MaxFragmentAtomicCounterBuffers", type="int"
        ),
        "gl_MaxCombinedImageUniforms": Var(
            name="gl_MaxCombinedImageUniforms", type="int"
        ),
        "gl_MaxCombinedAtomicCounters": Var(
            name="gl_MaxCombinedAtomicCounters", type="int"
        ),
        "gl_MaxCombinedAtomicCounterBuffers": Var(
            name="gl_MaxCombinedAtomicCounterBuffers", type="int"
        ),
        "gl_MaxImageUnits": Var(name="gl_MaxImageUnits", type="int"),
        "gl_MaxCombinedImageUnitsAndFragmentOutputs": Var(
            name="gl_MaxCombinedImageUnitsAndFragmentOutputs", type="int"
        ),
        "gl_MaxImageSamples": Var(name="gl_MaxImageSamples", type="int"),
        "gl_MaxAtomicCounterBindings": Var(
            name="gl_MaxAtomicCounterBindings", type="int"
        ),
        "gl_MaxAtomicCounterBufferSize": Var(
            name="gl_MaxAtomicCounterBufferSize", type="int"
        ),
        "gl_MinProgramTexelOffset": Var(name="gl_MinProgramTexelOffset", type="int"),
        "gl_MaxProgramTexelOffset": Var(name="gl_MaxProgramTexelOffset", type="int"),
        "gl_MaxComputeWorkGroupCount": Var(
            name="gl_MaxComputeWorkGroupCount", type="ivec3"
        ),
        "gl_MaxComputeWorkGroupSize": Var(
            name="gl_MaxComputeWorkGroupSize", type="ivec3"
        ),
        "gl_MaxComputeUniformComponents": Var(
            name="gl_MaxComputeUniformComponents", type="int"
        ),
        "gl_MaxComputeTextureImageUnits": Var(
            name="gl_MaxComputeTextureImageUnits", type="int"
        ),
        "gl_MaxComputeImageUniforms": Var(
            name="gl_MaxComputeImageUniforms", type="int"
        ),
        "gl_MaxComputeAtomicCounters": Var(
            name="gl_MaxComputeAtomicCounters", type="int"
        ),
        "gl_MaxComputeAtomicCounterBuffers": Var(
            name="gl_MaxComputeAtomicCounterBuffers", type="int"
        ),
        "gl_MaxTransformFeedbackBuffers": Var(
            name="gl_MaxTransformFeedbackBuffers", type="int"
        ),
        "gl_MaxTransformFeedbackInterleavedComponents": Var(
            name="gl_MaxTransformFeedbackInterleavedComponents", type="int"
        ),
    }

    function_groups = {}
    functions = {
        "abs(float)": Func(
            return_type="float",
            name="abs",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "abs(vec2)": Func(
            return_type="vec2",
            name="abs",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "abs(vec3)": Func(
            return_type="vec3",
            name="abs",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "abs(vec4)": Func(
            return_type="vec4",
            name="abs",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "abs(int)": Func(
            return_type="int",
            name="abs",
            args=[
                Var(name="x", type="int"),
            ],
        ),
        "abs(ivec2)": Func(
            return_type="ivec2",
            name="abs",
            args=[
                Var(name="x", type="ivec2"),
            ],
        ),
        "abs(ivec3)": Func(
            return_type="ivec3",
            name="abs",
            args=[
                Var(name="x", type="ivec3"),
            ],
        ),
        "abs(ivec4)": Func(
            return_type="ivec4",
            name="abs",
            args=[
                Var(name="x", type="ivec4"),
            ],
        ),
        "abs(double)": Func(
            return_type="double",
            name="abs",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "abs(dvec2)": Func(
            return_type="dvec2",
            name="abs",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "abs(dvec3)": Func(
            return_type="dvec3",
            name="abs",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "abs(dvec4)": Func(
            return_type="dvec4",
            name="abs",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "acos(float)": Func(
            return_type="float",
            name="acos",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "acos(vec2)": Func(
            return_type="vec2",
            name="acos",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "acos(vec3)": Func(
            return_type="vec3",
            name="acos",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "acos(vec4)": Func(
            return_type="vec4",
            name="acos",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "acosh(float)": Func(
            return_type="float",
            name="acosh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "acosh(vec2)": Func(
            return_type="vec2",
            name="acosh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "acosh(vec3)": Func(
            return_type="vec3",
            name="acosh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "acosh(vec4)": Func(
            return_type="vec4",
            name="acosh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "all(bvec2)": Func(
            return_type="bool",
            name="all",
            args=[
                Var(name="x", type="bvec2"),
            ],
        ),
        "all(bvec3)": Func(
            return_type="bool",
            name="all",
            args=[
                Var(name="x", type="bvec3"),
            ],
        ),
        "all(bvec4)": Func(
            return_type="bool",
            name="all",
            args=[
                Var(name="x", type="bvec4"),
            ],
        ),
        "any(bvec2)": Func(
            return_type="bool",
            name="any",
            args=[
                Var(name="x", type="bvec2"),
            ],
        ),
        "any(bvec3)": Func(
            return_type="bool",
            name="any",
            args=[
                Var(name="x", type="bvec3"),
            ],
        ),
        "any(bvec4)": Func(
            return_type="bool",
            name="any",
            args=[
                Var(name="x", type="bvec4"),
            ],
        ),
        "asin(float)": Func(
            return_type="float",
            name="asin",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "asin(vec2)": Func(
            return_type="vec2",
            name="asin",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "asin(vec3)": Func(
            return_type="vec3",
            name="asin",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "asin(vec4)": Func(
            return_type="vec4",
            name="asin",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "asinh(float)": Func(
            return_type="float",
            name="asinh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "asinh(vec2)": Func(
            return_type="vec2",
            name="asinh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "asinh(vec3)": Func(
            return_type="vec3",
            name="asinh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "asinh(vec4)": Func(
            return_type="vec4",
            name="asinh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "atan(float, float)": Func(
            return_type="float",
            name="atan",
            args=[
                Var(name="y", type="float"),
                Var(name="x", type="float"),
            ],
        ),
        "atan(vec2, vec2)": Func(
            return_type="vec2",
            name="atan",
            args=[
                Var(name="y", type="vec2"),
                Var(name="x", type="vec2"),
            ],
        ),
        "atan(vec3, vec3)": Func(
            return_type="vec3",
            name="atan",
            args=[
                Var(name="y", type="vec3"),
                Var(name="x", type="vec3"),
            ],
        ),
        "atan(vec4, vec4)": Func(
            return_type="vec4",
            name="atan",
            args=[
                Var(name="y", type="vec4"),
                Var(name="x", type="vec4"),
            ],
        ),
        "atan(float)": Func(
            return_type="float",
            name="atan",
            args=[
                Var(name="y_over_x", type="float"),
            ],
        ),
        "atan(vec2)": Func(
            return_type="vec2",
            name="atan",
            args=[
                Var(name="y_over_x", type="vec2"),
            ],
        ),
        "atan(vec3)": Func(
            return_type="vec3",
            name="atan",
            args=[
                Var(name="y_over_x", type="vec3"),
            ],
        ),
        "atan(vec4)": Func(
            return_type="vec4",
            name="atan",
            args=[
                Var(name="y_over_x", type="vec4"),
            ],
        ),
        "atanh(float)": Func(
            return_type="float",
            name="atanh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "atanh(vec2)": Func(
            return_type="vec2",
            name="atanh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "atanh(vec3)": Func(
            return_type="vec3",
            name="atanh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "atanh(vec4)": Func(
            return_type="vec4",
            name="atanh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "atomicAdd(int, int)": Func(
            return_type="int",
            name="atomicAdd",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicAdd(uint, uint)": Func(
            return_type="uint",
            name="atomicAdd",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicAnd(int, int)": Func(
            return_type="int",
            name="atomicAnd",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicAnd(uint, uint)": Func(
            return_type="uint",
            name="atomicAnd",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicCompSwap(int, uint, uint)": Func(
            return_type="int",
            name="atomicCompSwap",
            args=[
                Var(name="mem", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicCompSwap(uint, uint, uint)": Func(
            return_type="uint",
            name="atomicCompSwap",
            args=[
                Var(name="mem", type="uint"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicCounter(atomic_uint)": Func(
            return_type="uint",
            name="atomicCounter",
            args=[
                Var(name="c", type="atomic_uint"),
            ],
        ),
        "atomicCounterDecrement(atomic_uint)": Func(
            return_type="uint",
            name="atomicCounterDecrement",
            args=[
                Var(name="c", type="atomic_uint"),
            ],
        ),
        "atomicCounterIncrement(atomic_uint)": Func(
            return_type="uint",
            name="atomicCounterIncrement",
            args=[
                Var(name="c", type="atomic_uint"),
            ],
        ),
        "atomicExchange(int, int)": Func(
            return_type="int",
            name="atomicExchange",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicExchange(uint, uint)": Func(
            return_type="uint",
            name="atomicExchange",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicMax(int, int)": Func(
            return_type="int",
            name="atomicMax",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicMax(uint, uint)": Func(
            return_type="uint",
            name="atomicMax",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicMin(int, int)": Func(
            return_type="int",
            name="atomicMin",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicMin(uint, uint)": Func(
            return_type="uint",
            name="atomicMin",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicOr(int, int)": Func(
            return_type="int",
            name="atomicOr",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicOr(uint, uint)": Func(
            return_type="uint",
            name="atomicOr",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "atomicXor(int, int)": Func(
            return_type="int",
            name="atomicXor",
            args=[
                Var(name="mem", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "atomicXor(uint, uint)": Func(
            return_type="uint",
            name="atomicXor",
            args=[
                Var(name="mem", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "barrier()": Func(return_type="void", name="barrier", args=[]),
        "bitCount(int)": Func(
            return_type="int",
            name="bitCount",
            args=[
                Var(name="value", type="int"),
            ],
        ),
        "bitCount(ivec2)": Func(
            return_type="ivec2",
            name="bitCount",
            args=[
                Var(name="value", type="ivec2"),
            ],
        ),
        "bitCount(ivec3)": Func(
            return_type="ivec3",
            name="bitCount",
            args=[
                Var(name="value", type="ivec3"),
            ],
        ),
        "bitCount(ivec4)": Func(
            return_type="ivec4",
            name="bitCount",
            args=[
                Var(name="value", type="ivec4"),
            ],
        ),
        "bitCount(uint)": Func(
            return_type="int",
            name="bitCount",
            args=[
                Var(name="value", type="uint"),
            ],
        ),
        "bitCount(uvec2)": Func(
            return_type="ivec2",
            name="bitCount",
            args=[
                Var(name="value", type="uvec2"),
            ],
        ),
        "bitCount(uvec3)": Func(
            return_type="ivec3",
            name="bitCount",
            args=[
                Var(name="value", type="uvec3"),
            ],
        ),
        "bitCount(uvec4)": Func(
            return_type="ivec4",
            name="bitCount",
            args=[
                Var(name="value", type="uvec4"),
            ],
        ),
        "bitfieldExtract(int, int, int)": Func(
            return_type="int",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="int"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(ivec2, int, int)": Func(
            return_type="ivec2",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="ivec2"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(ivec3, int, int)": Func(
            return_type="ivec3",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="ivec3"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(ivec4, int, int)": Func(
            return_type="ivec4",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="ivec4"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(uint, int, int)": Func(
            return_type="uint",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="uint"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(uvec2, int, int)": Func(
            return_type="uvec2",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="uvec2"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(uvec3, int, int)": Func(
            return_type="uvec3",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="uvec3"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldExtract(uvec4, int, int)": Func(
            return_type="uvec4",
            name="bitfieldExtract",
            args=[
                Var(name="value", type="uvec4"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(int, int, int, int)": Func(
            return_type="int",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="int"),
                Var(name="insert", type="int"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(ivec2, ivec2, int, int)": Func(
            return_type="ivec2",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="ivec2"),
                Var(name="insert", type="ivec2"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(ivec3, ivec3, int, int)": Func(
            return_type="ivec3",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="ivec3"),
                Var(name="insert", type="ivec3"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(ivec4, ivec4, int, int)": Func(
            return_type="ivec4",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="ivec4"),
                Var(name="insert", type="ivec4"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(uint, uint, int, int)": Func(
            return_type="uint",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="uint"),
                Var(name="insert", type="uint"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(uvec2, uvec2, int, int)": Func(
            return_type="uvec2",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="uvec2"),
                Var(name="insert", type="uvec2"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(uvec3, uvec3, int, int)": Func(
            return_type="uvec3",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="uvec3"),
                Var(name="insert", type="uvec3"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldInsert(uvec4, uvec4, int, int)": Func(
            return_type="uvec4",
            name="bitfieldInsert",
            args=[
                Var(name="base", type="uvec4"),
                Var(name="insert", type="uvec4"),
                Var(name="offset", type="int"),
                Var(name="bits", type="int"),
            ],
        ),
        "bitfieldReverse(int)": Func(
            return_type="int",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="int"),
            ],
        ),
        "bitfieldReverse(ivec2)": Func(
            return_type="ivec2",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="ivec2"),
            ],
        ),
        "bitfieldReverse(ivec3)": Func(
            return_type="ivec3",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="ivec3"),
            ],
        ),
        "bitfieldReverse(ivec4)": Func(
            return_type="ivec4",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="ivec4"),
            ],
        ),
        "bitfieldReverse(uint)": Func(
            return_type="uint",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="uint"),
            ],
        ),
        "bitfieldReverse(uvec2)": Func(
            return_type="uvec2",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="uvec2"),
            ],
        ),
        "bitfieldReverse(uvec3)": Func(
            return_type="uvec3",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="uvec3"),
            ],
        ),
        "bitfieldReverse(uvec4)": Func(
            return_type="uvec4",
            name="bitfieldReverse",
            args=[
                Var(name="value", type="uvec4"),
            ],
        ),
        "ceil(float)": Func(
            return_type="float",
            name="ceil",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "ceil(vec2)": Func(
            return_type="vec2",
            name="ceil",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "ceil(vec3)": Func(
            return_type="vec3",
            name="ceil",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "ceil(vec4)": Func(
            return_type="vec4",
            name="ceil",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "ceil(double)": Func(
            return_type="double",
            name="ceil",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "ceil(dvec2)": Func(
            return_type="dvec2",
            name="ceil",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "ceil(dvec3)": Func(
            return_type="dvec3",
            name="ceil",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "ceil(dvec4)": Func(
            return_type="dvec4",
            name="ceil",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "clamp(float, float, float)": Func(
            return_type="float",
            name="clamp",
            args=[
                Var(name="x", type="float"),
                Var(name="minVal", type="float"),
                Var(name="maxVal", type="float"),
            ],
        ),
        "clamp(vec2, vec2, vec2)": Func(
            return_type="vec2",
            name="clamp",
            args=[
                Var(name="x", type="vec2"),
                Var(name="minVal", type="vec2"),
                Var(name="maxVal", type="vec2"),
            ],
        ),
        "clamp(vec3, vec3, vec3)": Func(
            return_type="vec3",
            name="clamp",
            args=[
                Var(name="x", type="vec3"),
                Var(name="minVal", type="vec3"),
                Var(name="maxVal", type="vec3"),
            ],
        ),
        "clamp(vec4, vec4, vec4)": Func(
            return_type="vec4",
            name="clamp",
            args=[
                Var(name="x", type="vec4"),
                Var(name="minVal", type="vec4"),
                Var(name="maxVal", type="vec4"),
            ],
        ),
        "clamp(vec2, float, float)": Func(
            return_type="vec2",
            name="clamp",
            args=[
                Var(name="x", type="vec2"),
                Var(name="minVal", type="float"),
                Var(name="maxVal", type="float"),
            ],
        ),
        "clamp(vec3, float, float)": Func(
            return_type="vec3",
            name="clamp",
            args=[
                Var(name="x", type="vec3"),
                Var(name="minVal", type="float"),
                Var(name="maxVal", type="float"),
            ],
        ),
        "clamp(vec4, float, float)": Func(
            return_type="vec4",
            name="clamp",
            args=[
                Var(name="x", type="vec4"),
                Var(name="minVal", type="float"),
                Var(name="maxVal", type="float"),
            ],
        ),
        "clamp(double, double, double)": Func(
            return_type="double",
            name="clamp",
            args=[
                Var(name="x", type="double"),
                Var(name="minVal", type="double"),
                Var(name="maxVal", type="double"),
            ],
        ),
        "clamp(dvec2, dvec2, dvec2)": Func(
            return_type="dvec2",
            name="clamp",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="minVal", type="dvec2"),
                Var(name="maxVal", type="dvec2"),
            ],
        ),
        "clamp(dvec3, dvec3, dvec3)": Func(
            return_type="dvec3",
            name="clamp",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="minVal", type="dvec3"),
                Var(name="maxVal", type="dvec3"),
            ],
        ),
        "clamp(dvec4, dvec4, dvec4)": Func(
            return_type="dvec4",
            name="clamp",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="minVal", type="dvec4"),
                Var(name="maxVal", type="dvec4"),
            ],
        ),
        "clamp(dvec2, double, double)": Func(
            return_type="dvec2",
            name="clamp",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="minVal", type="double"),
                Var(name="maxVal", type="double"),
            ],
        ),
        "clamp(dvec3, double, double)": Func(
            return_type="dvec3",
            name="clamp",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="minVal", type="double"),
                Var(name="maxVal", type="double"),
            ],
        ),
        "clamp(dvec4, double, double)": Func(
            return_type="dvec4",
            name="clamp",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="minVal", type="double"),
                Var(name="maxVal", type="double"),
            ],
        ),
        "clamp(int, int, int)": Func(
            return_type="int",
            name="clamp",
            args=[
                Var(name="x", type="int"),
                Var(name="minVal", type="int"),
                Var(name="maxVal", type="int"),
            ],
        ),
        "clamp(ivec2, ivec2, ivec2)": Func(
            return_type="ivec2",
            name="clamp",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="minVal", type="ivec2"),
                Var(name="maxVal", type="ivec2"),
            ],
        ),
        "clamp(ivec3, ivec3, ivec3)": Func(
            return_type="ivec3",
            name="clamp",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="minVal", type="ivec3"),
                Var(name="maxVal", type="ivec3"),
            ],
        ),
        "clamp(ivec4, ivec4, ivec4)": Func(
            return_type="ivec4",
            name="clamp",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="minVal", type="ivec4"),
                Var(name="maxVal", type="ivec4"),
            ],
        ),
        "clamp(ivec2, int, int)": Func(
            return_type="ivec2",
            name="clamp",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="minVal", type="int"),
                Var(name="maxVal", type="int"),
            ],
        ),
        "clamp(ivec3, int, int)": Func(
            return_type="ivec3",
            name="clamp",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="minVal", type="int"),
                Var(name="maxVal", type="int"),
            ],
        ),
        "clamp(ivec4, int, int)": Func(
            return_type="ivec4",
            name="clamp",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="minVal", type="int"),
                Var(name="maxVal", type="int"),
            ],
        ),
        "clamp(uint, uint, uint)": Func(
            return_type="uint",
            name="clamp",
            args=[
                Var(name="x", type="uint"),
                Var(name="minVal", type="uint"),
                Var(name="maxVal", type="uint"),
            ],
        ),
        "clamp(uvec2, uvec2, uvec2)": Func(
            return_type="uvec2",
            name="clamp",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="minVal", type="uvec2"),
                Var(name="maxVal", type="uvec2"),
            ],
        ),
        "clamp(uvec3, uvec3, uvec3)": Func(
            return_type="uvec3",
            name="clamp",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="minVal", type="uvec3"),
                Var(name="maxVal", type="uvec3"),
            ],
        ),
        "clamp(uvec4, uvec4, uvec4)": Func(
            return_type="uvec4",
            name="clamp",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="minVal", type="uvec4"),
                Var(name="maxVal", type="uvec4"),
            ],
        ),
        "clamp(uvec2, uint, uint)": Func(
            return_type="uvec2",
            name="clamp",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="minVal", type="uint"),
                Var(name="maxVal", type="uint"),
            ],
        ),
        "clamp(uvec3, uint, uint)": Func(
            return_type="uvec3",
            name="clamp",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="minVal", type="uint"),
                Var(name="maxVal", type="uint"),
            ],
        ),
        "clamp(uvec4, uint, uint)": Func(
            return_type="uvec4",
            name="clamp",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="minVal", type="uint"),
                Var(name="maxVal", type="uint"),
            ],
        ),
        "cos(float)": Func(
            return_type="float",
            name="cos",
            args=[
                Var(name="angle", type="float"),
            ],
        ),
        "cos(vec2)": Func(
            return_type="vec2",
            name="cos",
            args=[
                Var(name="angle", type="vec2"),
            ],
        ),
        "cos(vec3)": Func(
            return_type="vec3",
            name="cos",
            args=[
                Var(name="angle", type="vec3"),
            ],
        ),
        "cos(vec4)": Func(
            return_type="vec4",
            name="cos",
            args=[
                Var(name="angle", type="vec4"),
            ],
        ),
        "cosh(float)": Func(
            return_type="float",
            name="cosh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "cosh(vec2)": Func(
            return_type="vec2",
            name="cosh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "cosh(vec3)": Func(
            return_type="vec3",
            name="cosh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "cosh(vec4)": Func(
            return_type="vec4",
            name="cosh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "cross(vec3, vec3)": Func(
            return_type="vec3",
            name="cross",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "cross(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="cross",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
            ],
        ),
        "degrees(float)": Func(
            return_type="float",
            name="degrees",
            args=[
                Var(name="radians", type="float"),
            ],
        ),
        "degrees(vec2)": Func(
            return_type="vec2",
            name="degrees",
            args=[
                Var(name="radians", type="vec2"),
            ],
        ),
        "degrees(vec3)": Func(
            return_type="vec3",
            name="degrees",
            args=[
                Var(name="radians", type="vec3"),
            ],
        ),
        "degrees(vec4)": Func(
            return_type="vec4",
            name="degrees",
            args=[
                Var(name="radians", type="vec4"),
            ],
        ),
        "determinant(mat2)": Func(
            return_type="float",
            name="determinant",
            args=[
                Var(name="m", type="mat2"),
            ],
        ),
        "determinant(mat3)": Func(
            return_type="float",
            name="determinant",
            args=[
                Var(name="m", type="mat3"),
            ],
        ),
        "determinant(mat4)": Func(
            return_type="float",
            name="determinant",
            args=[
                Var(name="m", type="mat4"),
            ],
        ),
        "determinant(dmat2)": Func(
            return_type="double",
            name="determinant",
            args=[
                Var(name="m", type="dmat2"),
            ],
        ),
        "determinant(dmat3)": Func(
            return_type="double",
            name="determinant",
            args=[
                Var(name="m", type="dmat3"),
            ],
        ),
        "determinant(dmat4)": Func(
            return_type="double",
            name="determinant",
            args=[
                Var(name="m", type="dmat4"),
            ],
        ),
        "dFdx(float)": Func(
            return_type="float",
            name="dFdx",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdx(vec2)": Func(
            return_type="vec2",
            name="dFdx",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdx(vec3)": Func(
            return_type="vec3",
            name="dFdx",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdx(vec4)": Func(
            return_type="vec4",
            name="dFdx",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "dFdy(float)": Func(
            return_type="float",
            name="dFdy",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdy(vec2)": Func(
            return_type="vec2",
            name="dFdy",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdy(vec3)": Func(
            return_type="vec3",
            name="dFdy",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdy(vec4)": Func(
            return_type="vec4",
            name="dFdy",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "dFdxCoarse(float)": Func(
            return_type="float",
            name="dFdxCoarse",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdxCoarse(vec2)": Func(
            return_type="vec2",
            name="dFdxCoarse",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdxCoarse(vec3)": Func(
            return_type="vec3",
            name="dFdxCoarse",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdxCoarse(vec4)": Func(
            return_type="vec4",
            name="dFdxCoarse",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "dFdyCoarse(float)": Func(
            return_type="float",
            name="dFdyCoarse",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdyCoarse(vec2)": Func(
            return_type="vec2",
            name="dFdyCoarse",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdyCoarse(vec3)": Func(
            return_type="vec3",
            name="dFdyCoarse",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdyCoarse(vec4)": Func(
            return_type="vec4",
            name="dFdyCoarse",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "dFdxFine(float)": Func(
            return_type="float",
            name="dFdxFine",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdxFine(vec2)": Func(
            return_type="vec2",
            name="dFdxFine",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdxFine(vec3)": Func(
            return_type="vec3",
            name="dFdxFine",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdxFine(vec4)": Func(
            return_type="vec4",
            name="dFdxFine",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "dFdyFine(float)": Func(
            return_type="float",
            name="dFdyFine",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "dFdyFine(vec2)": Func(
            return_type="vec2",
            name="dFdyFine",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "dFdyFine(vec3)": Func(
            return_type="vec3",
            name="dFdyFine",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "dFdyFine(vec4)": Func(
            return_type="vec4",
            name="dFdyFine",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "distance(float, float)": Func(
            return_type="float",
            name="distance",
            args=[
                Var(name="p0", type="float"),
                Var(name="p1", type="float"),
            ],
        ),
        "distance(vec2, vec2)": Func(
            return_type="float",
            name="distance",
            args=[
                Var(name="p0", type="vec2"),
                Var(name="p1", type="vec2"),
            ],
        ),
        "distance(vec3, vec3)": Func(
            return_type="float",
            name="distance",
            args=[
                Var(name="p0", type="vec3"),
                Var(name="p1", type="vec3"),
            ],
        ),
        "distance(vec4, vec4)": Func(
            return_type="float",
            name="distance",
            args=[
                Var(name="p0", type="vec4"),
                Var(name="p1", type="vec4"),
            ],
        ),
        "distance(double, double)": Func(
            return_type="double",
            name="distance",
            args=[
                Var(name="p0", type="double"),
                Var(name="p1", type="double"),
            ],
        ),
        "distance(dvec2, dvec2)": Func(
            return_type="double",
            name="distance",
            args=[
                Var(name="p0", type="dvec2"),
                Var(name="p1", type="dvec2"),
            ],
        ),
        "distance(dvec3, dvec3)": Func(
            return_type="double",
            name="distance",
            args=[
                Var(name="p0", type="dvec3"),
                Var(name="p1", type="dvec3"),
            ],
        ),
        "distance(dvec4, dvec4)": Func(
            return_type="double",
            name="distance",
            args=[
                Var(name="p0", type="dvec4"),
                Var(name="p1", type="dvec4"),
            ],
        ),
        "dot(float, float)": Func(
            return_type="float",
            name="dot",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
            ],
        ),
        "dot(vec2, vec2)": Func(
            return_type="float",
            name="dot",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "dot(vec3, vec3)": Func(
            return_type="float",
            name="dot",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "dot(vec4, vec4)": Func(
            return_type="float",
            name="dot",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "dot(double, double)": Func(
            return_type="double",
            name="dot",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
            ],
        ),
        "dot(dvec2, dvec2)": Func(
            return_type="double",
            name="dot",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
            ],
        ),
        "dot(dvec3, dvec3)": Func(
            return_type="double",
            name="dot",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
            ],
        ),
        "dot(dvec4, dvec4)": Func(
            return_type="double",
            name="dot",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
            ],
        ),
        "EmitStreamVertex(int)": Func(
            return_type="void",
            name="EmitStreamVertex",
            args=[
                Var(name="stream", type="int"),
            ],
        ),
        "EmitVertex()": Func(return_type="void", name="EmitVertex", args=[]),
        "EndPrimitive()": Func(return_type="void", name="EndPrimitive", args=[]),
        "EndStreamPrimitive(int)": Func(
            return_type="void",
            name="EndStreamPrimitive",
            args=[
                Var(name="stream", type="int"),
            ],
        ),
        "equal(vec2, vec2)": Func(
            return_type="bvec2",
            name="equal",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "equal(vec3, vec3)": Func(
            return_type="bvec3",
            name="equal",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "equal(vec4, vec4)": Func(
            return_type="bvec4",
            name="equal",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "equal(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="equal",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "equal(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="equal",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "equal(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="equal",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "equal(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="equal",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "equal(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="equal",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "equal(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="equal",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "exp(float)": Func(
            return_type="float",
            name="exp",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "exp(vec2)": Func(
            return_type="vec2",
            name="exp",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "exp(vec3)": Func(
            return_type="vec3",
            name="exp",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "exp(vec4)": Func(
            return_type="vec4",
            name="exp",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "exp2(float)": Func(
            return_type="float",
            name="exp2",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "exp2(vec2)": Func(
            return_type="vec2",
            name="exp2",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "exp2(vec3)": Func(
            return_type="vec3",
            name="exp2",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "exp2(vec4)": Func(
            return_type="vec4",
            name="exp2",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "faceforward(float, float, float)": Func(
            return_type="float",
            name="faceforward",
            args=[
                Var(name="N", type="float"),
                Var(name="I", type="float"),
                Var(name="Nref", type="float"),
            ],
        ),
        "faceforward(vec2, vec2, vec2)": Func(
            return_type="vec2",
            name="faceforward",
            args=[
                Var(name="N", type="vec2"),
                Var(name="I", type="vec2"),
                Var(name="Nref", type="vec2"),
            ],
        ),
        "faceforward(vec3, vec3, vec3)": Func(
            return_type="vec3",
            name="faceforward",
            args=[
                Var(name="N", type="vec3"),
                Var(name="I", type="vec3"),
                Var(name="Nref", type="vec3"),
            ],
        ),
        "faceforward(vec4, vec4, vec4)": Func(
            return_type="vec4",
            name="faceforward",
            args=[
                Var(name="N", type="vec4"),
                Var(name="I", type="vec4"),
                Var(name="Nref", type="vec4"),
            ],
        ),
        "faceforward(double, double, double)": Func(
            return_type="double",
            name="faceforward",
            args=[
                Var(name="N", type="double"),
                Var(name="I", type="double"),
                Var(name="Nref", type="double"),
            ],
        ),
        "faceforward(dvec2, dvec2, dvec2)": Func(
            return_type="dvec2",
            name="faceforward",
            args=[
                Var(name="N", type="dvec2"),
                Var(name="I", type="dvec2"),
                Var(name="Nref", type="dvec2"),
            ],
        ),
        "faceforward(dvec3, dvec3, dvec3)": Func(
            return_type="dvec3",
            name="faceforward",
            args=[
                Var(name="N", type="dvec3"),
                Var(name="I", type="dvec3"),
                Var(name="Nref", type="dvec3"),
            ],
        ),
        "faceforward(dvec4, dvec4, dvec4)": Func(
            return_type="dvec4",
            name="faceforward",
            args=[
                Var(name="N", type="dvec4"),
                Var(name="I", type="dvec4"),
                Var(name="Nref", type="dvec4"),
            ],
        ),
        "findLSB(int)": Func(
            return_type="int",
            name="findLSB",
            args=[
                Var(name="value", type="int"),
            ],
        ),
        "findLSB(ivec2)": Func(
            return_type="ivec2",
            name="findLSB",
            args=[
                Var(name="value", type="ivec2"),
            ],
        ),
        "findLSB(ivec3)": Func(
            return_type="ivec3",
            name="findLSB",
            args=[
                Var(name="value", type="ivec3"),
            ],
        ),
        "findLSB(ivec4)": Func(
            return_type="ivec4",
            name="findLSB",
            args=[
                Var(name="value", type="ivec4"),
            ],
        ),
        "findLSB(uint)": Func(
            return_type="int",
            name="findLSB",
            args=[
                Var(name="value", type="uint"),
            ],
        ),
        "findLSB(uvec2)": Func(
            return_type="ivec2",
            name="findLSB",
            args=[
                Var(name="value", type="uvec2"),
            ],
        ),
        "findLSB(uvec3)": Func(
            return_type="ivec3",
            name="findLSB",
            args=[
                Var(name="value", type="uvec3"),
            ],
        ),
        "findLSB(uvec4)": Func(
            return_type="ivec4",
            name="findLSB",
            args=[
                Var(name="value", type="uvec4"),
            ],
        ),
        "findMSB(int)": Func(
            return_type="int",
            name="findMSB",
            args=[
                Var(name="value", type="int"),
            ],
        ),
        "findMSB(ivec2)": Func(
            return_type="ivec2",
            name="findMSB",
            args=[
                Var(name="value", type="ivec2"),
            ],
        ),
        "findMSB(ivec3)": Func(
            return_type="ivec3",
            name="findMSB",
            args=[
                Var(name="value", type="ivec3"),
            ],
        ),
        "findMSB(ivec4)": Func(
            return_type="ivec4",
            name="findMSB",
            args=[
                Var(name="value", type="ivec4"),
            ],
        ),
        "findMSB(uint)": Func(
            return_type="int",
            name="findMSB",
            args=[
                Var(name="value", type="uint"),
            ],
        ),
        "findMSB(uvec2)": Func(
            return_type="ivec2",
            name="findMSB",
            args=[
                Var(name="value", type="uvec2"),
            ],
        ),
        "findMSB(uvec3)": Func(
            return_type="ivec3",
            name="findMSB",
            args=[
                Var(name="value", type="uvec3"),
            ],
        ),
        "findMSB(uvec4)": Func(
            return_type="ivec4",
            name="findMSB",
            args=[
                Var(name="value", type="uvec4"),
            ],
        ),
        "floatBitsToInt(float)": Func(
            return_type="int",
            name="floatBitsToInt",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "floatBitsToInt(vec2)": Func(
            return_type="ivec2",
            name="floatBitsToInt",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "floatBitsToInt(vec3)": Func(
            return_type="ivec3",
            name="floatBitsToInt",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "floatBitsToInt(vec4)": Func(
            return_type="ivec4",
            name="floatBitsToInt",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "floatBitsToUint(float)": Func(
            return_type="uint",
            name="floatBitsToUint",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "floatBitsToUint(vec2)": Func(
            return_type="uvec2",
            name="floatBitsToUint",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "floatBitsToUint(vec3)": Func(
            return_type="uvec3",
            name="floatBitsToUint",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "floatBitsToUint(vec4)": Func(
            return_type="uvec4",
            name="floatBitsToUint",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "floor(float)": Func(
            return_type="float",
            name="floor",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "floor(vec2)": Func(
            return_type="vec2",
            name="floor",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "floor(vec3)": Func(
            return_type="vec3",
            name="floor",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "floor(vec4)": Func(
            return_type="vec4",
            name="floor",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "floor(double)": Func(
            return_type="double",
            name="floor",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "floor(dvec2)": Func(
            return_type="dvec2",
            name="floor",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "floor(dvec3)": Func(
            return_type="dvec3",
            name="floor",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "floor(dvec4)": Func(
            return_type="dvec4",
            name="floor",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "fma(float, float, float)": Func(
            return_type="float",
            name="fma",
            args=[
                Var(name="a", type="float"),
                Var(name="b", type="float"),
                Var(name="c", type="float"),
            ],
        ),
        "fma(vec2, vec2, vec2)": Func(
            return_type="vec2",
            name="fma",
            args=[
                Var(name="a", type="vec2"),
                Var(name="b", type="vec2"),
                Var(name="c", type="vec2"),
            ],
        ),
        "fma(vec3, vec3, vec3)": Func(
            return_type="vec3",
            name="fma",
            args=[
                Var(name="a", type="vec3"),
                Var(name="b", type="vec3"),
                Var(name="c", type="vec3"),
            ],
        ),
        "fma(vec4, vec4, vec4)": Func(
            return_type="vec4",
            name="fma",
            args=[
                Var(name="a", type="vec4"),
                Var(name="b", type="vec4"),
                Var(name="c", type="vec4"),
            ],
        ),
        "fma(double, double, double)": Func(
            return_type="double",
            name="fma",
            args=[
                Var(name="a", type="double"),
                Var(name="b", type="double"),
                Var(name="c", type="double"),
            ],
        ),
        "fma(dvec2, dvec2, dvec2)": Func(
            return_type="dvec2",
            name="fma",
            args=[
                Var(name="a", type="dvec2"),
                Var(name="b", type="dvec2"),
                Var(name="c", type="dvec2"),
            ],
        ),
        "fma(dvec3, dvec3, dvec3)": Func(
            return_type="dvec3",
            name="fma",
            args=[
                Var(name="a", type="dvec3"),
                Var(name="b", type="dvec3"),
                Var(name="c", type="dvec3"),
            ],
        ),
        "fma(dvec4, dvec4, dvec4)": Func(
            return_type="dvec4",
            name="fma",
            args=[
                Var(name="a", type="dvec4"),
                Var(name="b", type="dvec4"),
                Var(name="c", type="dvec4"),
            ],
        ),
        "fract(float)": Func(
            return_type="float",
            name="fract",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "fract(vec2)": Func(
            return_type="vec2",
            name="fract",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "fract(vec3)": Func(
            return_type="vec3",
            name="fract",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "fract(vec4)": Func(
            return_type="vec4",
            name="fract",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "fract(double)": Func(
            return_type="double",
            name="fract",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "fract(dvec2)": Func(
            return_type="dvec2",
            name="fract",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "fract(dvec3)": Func(
            return_type="dvec3",
            name="fract",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "fract(dvec4)": Func(
            return_type="dvec4",
            name="fract",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "frexp(float, int)": Func(
            return_type="float",
            name="frexp",
            args=[
                Var(name="x", type="float"),
                Var(name="exp", type="int"),
            ],
        ),
        "frexp(vec2, ivec2)": Func(
            return_type="vec2",
            name="frexp",
            args=[
                Var(name="x", type="vec2"),
                Var(name="exp", type="ivec2"),
            ],
        ),
        "frexp(vec3, ivec3)": Func(
            return_type="vec3",
            name="frexp",
            args=[
                Var(name="x", type="vec3"),
                Var(name="exp", type="ivec3"),
            ],
        ),
        "frexp(vec4, ivec4)": Func(
            return_type="vec4",
            name="frexp",
            args=[
                Var(name="x", type="vec4"),
                Var(name="exp", type="ivec4"),
            ],
        ),
        "frexp(double, int)": Func(
            return_type="double",
            name="frexp",
            args=[
                Var(name="x", type="double"),
                Var(name="exp", type="int"),
            ],
        ),
        "frexp(dvec2, ivec2)": Func(
            return_type="dvec2",
            name="frexp",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="exp", type="ivec2"),
            ],
        ),
        "frexp(dvec3, ivec3)": Func(
            return_type="dvec3",
            name="frexp",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="exp", type="ivec3"),
            ],
        ),
        "frexp(dvec4, ivec4)": Func(
            return_type="dvec4",
            name="frexp",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="exp", type="ivec4"),
            ],
        ),
        "fwidth(float)": Func(
            return_type="float",
            name="fwidth",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "fwidth(vec2)": Func(
            return_type="vec2",
            name="fwidth",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "fwidth(vec3)": Func(
            return_type="vec3",
            name="fwidth",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "fwidth(vec4)": Func(
            return_type="vec4",
            name="fwidth",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "fwidthCoarse(float)": Func(
            return_type="float",
            name="fwidthCoarse",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "fwidthCoarse(vec2)": Func(
            return_type="vec2",
            name="fwidthCoarse",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "fwidthCoarse(vec3)": Func(
            return_type="vec3",
            name="fwidthCoarse",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "fwidthCoarse(vec4)": Func(
            return_type="vec4",
            name="fwidthCoarse",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "fwidthFine(float)": Func(
            return_type="float",
            name="fwidthFine",
            args=[
                Var(name="p", type="float"),
            ],
        ),
        "fwidthFine(vec2)": Func(
            return_type="vec2",
            name="fwidthFine",
            args=[
                Var(name="p", type="vec2"),
            ],
        ),
        "fwidthFine(vec3)": Func(
            return_type="vec3",
            name="fwidthFine",
            args=[
                Var(name="p", type="vec3"),
            ],
        ),
        "fwidthFine(vec4)": Func(
            return_type="vec4",
            name="fwidthFine",
            args=[
                Var(name="p", type="vec4"),
            ],
        ),
        "greaterThan(vec2, vec2)": Func(
            return_type="bvec2",
            name="greaterThan",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "greaterThan(vec3, vec3)": Func(
            return_type="bvec3",
            name="greaterThan",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "greaterThan(vec4, vec4)": Func(
            return_type="bvec4",
            name="greaterThan",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "greaterThan(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="greaterThan",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "greaterThan(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="greaterThan",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "greaterThan(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="greaterThan",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "greaterThan(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="greaterThan",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "greaterThan(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="greaterThan",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "greaterThan(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="greaterThan",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "greaterThanEqual(vec2, vec2)": Func(
            return_type="bvec2",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "greaterThanEqual(vec3, vec3)": Func(
            return_type="bvec3",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "greaterThanEqual(vec4, vec4)": Func(
            return_type="bvec4",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "greaterThanEqual(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "greaterThanEqual(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "greaterThanEqual(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "greaterThanEqual(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "greaterThanEqual(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "greaterThanEqual(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="greaterThanEqual",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "groupMemoryBarrier()": Func(
            return_type="void", name="groupMemoryBarrier", args=[]
        ),
        "imageAtomicAdd(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAdd(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAdd(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAdd",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicAnd(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicAnd(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicAnd",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image1D, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage1D, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage1D, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image2D, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage2D, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage2D, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image3D, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage3D, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage3D, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image2DRect, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DRect, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(imageCube, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimageCube, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimageCube, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(imageBuffer, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimageBuffer, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimageBuffer, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image1DArray, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage1DArray, ivec2, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image2DArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(imageCubeArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimageCubeArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimageCubeArray, ivec3, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image2DMS, ivec2, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DMS, ivec2, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DMS, ivec2, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image2DMSArray, ivec3, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DMSArray, ivec3, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DMSArray, ivec3, int, uint, uint)": Func(
            return_type="uint",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="uint"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicCompSwap(image1D, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage1D, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage1D, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image2D, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage2D, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage2D, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image3D, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage3D, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage3D, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image2DRect, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DRect, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(imageCube, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimageCube, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimageCube, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(imageBuffer, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimageBuffer, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimageBuffer, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image1DArray, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage1DArray, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image2DArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(imageCubeArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimageCubeArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimageCubeArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image2DMS, ivec2, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DMS, ivec2, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DMS, ivec2, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(image2DMSArray, ivec3, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(iimage2DMSArray, ivec3, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicCompSwap(uimage2DMSArray, ivec3, int, int, int)": Func(
            return_type="int",
            name="imageAtomicCompSwap",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="compare", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicExchange(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicExchange(image1D, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage1D, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage1D, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image2D, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage2D, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage2D, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image3D, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage3D, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage3D, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image2DRect, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage2DRect, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(imageCube, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimageCube, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimageCube, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(imageBuffer, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimageBuffer, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimageBuffer, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image1DArray, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage1DArray, ivec2, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image2DArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage2DArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage2DArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(imageCubeArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimageCubeArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimageCubeArray, ivec3, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image2DMS, ivec2, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage2DMS, ivec2, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage2DMS, ivec2, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(image2DMSArray, ivec3, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(iimage2DMSArray, ivec3, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicExchange(uimage2DMSArray, ivec3, int, float)": Func(
            return_type="int",
            name="imageAtomicExchange",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="float"),
            ],
        ),
        "imageAtomicMax(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMax(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMax(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMax",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicMin(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicMin(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicMin",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicOr(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicOr(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicOr",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage1D, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage2D, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage3D, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage2DRect, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(imageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimageCube, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(imageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimageBuffer, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage1DArray, ivec2, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage2DArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(imageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimageCubeArray, ivec3, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage2DMS, ivec2, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(iimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(uimage2DMSArray, ivec3, int, uint)": Func(
            return_type="uint",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uint"),
            ],
        ),
        "imageAtomicXor(image1D, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage1D, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage2D, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage3D, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage2DRect, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(imageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimageCube, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(imageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimageBuffer, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage1DArray, ivec2, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage2DArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(imageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimageCubeArray, ivec3, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage2DMS, ivec2, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(image2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(iimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageAtomicXor(uimage2DMSArray, ivec3, int, int)": Func(
            return_type="int",
            name="imageAtomicXor",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="int"),
            ],
        ),
        "imageLoad(image1D, int)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(iimage1D, int)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(uimage1D, int)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(image2D, ivec2)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(iimage2D, ivec2)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(uimage2D, ivec2)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(image3D, ivec3)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(iimage3D, ivec3)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(uimage3D, ivec3)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(image2DRect, ivec2)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(iimage2DRect, ivec2)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(imageCube, ivec3)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(iimageCube, ivec3)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(uimageCube, ivec3)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(imageBuffer, int)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(iimageBuffer, int)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(uimageBuffer, int)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "imageLoad(image1DArray, ivec2)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(iimage1DArray, ivec2)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "imageLoad(image2DArray, ivec3)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(iimage2DArray, ivec3)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(uimage2DArray, ivec3)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(imageCubeArray, ivec3)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(iimageCubeArray, ivec3)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(uimageCubeArray, ivec3)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
            ],
        ),
        "imageLoad(image2DMS, ivec2, int)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageLoad(iimage2DMS, ivec2, int)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageLoad(uimage2DMS, ivec2, int)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageLoad(image2DMSArray, ivec3, int)": Func(
            return_type="vec4",
            name="imageLoad",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageLoad(iimage2DMSArray, ivec3, int)": Func(
            return_type="ivec4",
            name="imageLoad",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageLoad(uimage2DMSArray, ivec3, int)": Func(
            return_type="uvec4",
            name="imageLoad",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "imageSamples(image2DMS)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="image2DMS"),
            ],
        ),
        "imageSamples(iimage2DMS)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="iimage2DMS"),
            ],
        ),
        "imageSamples(uimage2DMS)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="uimage2DMS"),
            ],
        ),
        "imageSamples(image2DMSArray)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="image2DMSArray"),
            ],
        ),
        "imageSamples(iimage2DMSArray)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="iimage2DMSArray"),
            ],
        ),
        "imageSamples(uimage2DMSArray)": Func(
            return_type="int",
            name="imageSamples",
            args=[
                Var(name="image", type="uimage2DMSArray"),
            ],
        ),
        "imageSize(image1D)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="image1D"),
            ],
        ),
        "imageSize(iimage1D)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="iimage1D"),
            ],
        ),
        "imageSize(uimage1D)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="uimage1D"),
            ],
        ),
        "imageSize(image2D)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="image2D"),
            ],
        ),
        "imageSize(iimage2D)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="iimage2D"),
            ],
        ),
        "imageSize(uimage2D)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="uimage2D"),
            ],
        ),
        "imageSize(image3D)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="image3D"),
            ],
        ),
        "imageSize(iimage3D)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="iimage3D"),
            ],
        ),
        "imageSize(uimage3D)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="uimage3D"),
            ],
        ),
        "imageSize(imageCube)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="imageCube"),
            ],
        ),
        "imageSize(iimageCube)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="iimageCube"),
            ],
        ),
        "imageSize(uimageCube)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="uimageCube"),
            ],
        ),
        "imageSize(imageCubeArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="imageCubeArray"),
            ],
        ),
        "imageSize(iimageCubeArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="iimageCubeArray"),
            ],
        ),
        "imageSize(uimageCubeArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="uimageCubeArray"),
            ],
        ),
        "imageSize(image2DRect)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="image2DRect"),
            ],
        ),
        "imageSize(iimage2DRect)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="iimage2DRect"),
            ],
        ),
        "imageSize(image1DArray)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="image1DArray"),
            ],
        ),
        "imageSize(iimage1DArray)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="iimage1DArray"),
            ],
        ),
        "imageSize(image2DArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="image2DArray"),
            ],
        ),
        "imageSize(iimage2DArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="iimage2DArray"),
            ],
        ),
        "imageSize(uimage2DArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="uimage2DArray"),
            ],
        ),
        "imageSize(imageBuffer)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="imageBuffer"),
            ],
        ),
        "imageSize(iimageBuffer)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="iimageBuffer"),
            ],
        ),
        "imageSize(uimageBuffer)": Func(
            return_type="int",
            name="imageSize",
            args=[
                Var(name="image", type="uimageBuffer"),
            ],
        ),
        "imageSize(image2DMS)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="image2DMS"),
            ],
        ),
        "imageSize(iimage2DMS)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="iimage2DMS"),
            ],
        ),
        "imageSize(uimage2DMS)": Func(
            return_type="ivec2",
            name="imageSize",
            args=[
                Var(name="image", type="uimage2DMS"),
            ],
        ),
        "imageSize(image2DMSArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="image2DMSArray"),
            ],
        ),
        "imageSize(iimage2DMSArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="iimage2DMSArray"),
            ],
        ),
        "imageSize(uimage2DMSArray)": Func(
            return_type="ivec3",
            name="imageSize",
            args=[
                Var(name="image", type="uimage2DMSArray"),
            ],
        ),
        "imageStore(image1D, int, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image1D"),
                Var(name="P", type="int"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage1D, int, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage1D, int, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage1D"),
                Var(name="P", type="int"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image2D, ivec2, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage2D, ivec2, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage2D, ivec2, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage2D"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image3D, ivec3, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage3D, ivec3, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage3D, ivec3, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage3D"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image2DRect, ivec2, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage2DRect, ivec2, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(iimage2DRect, ivec2, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(imageCube, ivec3, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="imageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimageCube, ivec3, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimageCube, ivec3, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimageCube"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(imageBuffer, int, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="imageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimageBuffer, int, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimageBuffer, int, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimageBuffer"),
                Var(name="P", type="int"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image1DArray, ivec2, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage1DArray, ivec2, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(iimage1DArray, ivec2, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image2DArray, ivec3, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage2DArray, ivec3, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage2DArray, ivec3, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(imageCubeArray, ivec3, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="imageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimageCubeArray, ivec3, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimageCubeArray, ivec3, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimageCubeArray"),
                Var(name="P", type="ivec3"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image2DMS, ivec2, int, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage2DMS, ivec2, int, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage2DMS, ivec2, int, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "imageStore(image2DMSArray, ivec3, int, vec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="image2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="vec4"),
            ],
        ),
        "imageStore(iimage2DMSArray, ivec3, int, ivec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="iimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="ivec4"),
            ],
        ),
        "imageStore(uimage2DMSArray, ivec3, int, uvec4)": Func(
            return_type="void",
            name="imageStore",
            args=[
                Var(name="image", type="uimage2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
                Var(name="data", type="uvec4"),
            ],
        ),
        "intBitsToFloat(int)": Func(
            return_type="float",
            name="intBitsToFloat",
            args=[
                Var(name="x", type="int"),
            ],
        ),
        "intBitsToFloat(ivec2)": Func(
            return_type="vec2",
            name="intBitsToFloat",
            args=[
                Var(name="x", type="ivec2"),
            ],
        ),
        "intBitsToFloat(ivec3)": Func(
            return_type="vec3",
            name="intBitsToFloat",
            args=[
                Var(name="x", type="ivec3"),
            ],
        ),
        "intBitsToFloat(ivec4)": Func(
            return_type="vec4",
            name="intBitsToFloat",
            args=[
                Var(name="x", type="ivec4"),
            ],
        ),
        "uintBitsToFloat(uint)": Func(
            return_type="float",
            name="uintBitsToFloat",
            args=[
                Var(name="x", type="uint"),
            ],
        ),
        "uintBitsToFloat(uvec2)": Func(
            return_type="vec2",
            name="uintBitsToFloat",
            args=[
                Var(name="x", type="uvec2"),
            ],
        ),
        "uintBitsToFloat(uvec3)": Func(
            return_type="vec3",
            name="uintBitsToFloat",
            args=[
                Var(name="x", type="uvec3"),
            ],
        ),
        "uintBitsToFloat(uvec4)": Func(
            return_type="vec4",
            name="uintBitsToFloat",
            args=[
                Var(name="x", type="uvec4"),
            ],
        ),
        "interpolateAtCentroid(float)": Func(
            return_type="float",
            name="interpolateAtCentroid",
            args=[
                Var(name="interpolant", type="float"),
            ],
        ),
        "interpolateAtCentroid(vec2)": Func(
            return_type="vec2",
            name="interpolateAtCentroid",
            args=[
                Var(name="interpolant", type="vec2"),
            ],
        ),
        "interpolateAtCentroid(vec3)": Func(
            return_type="vec3",
            name="interpolateAtCentroid",
            args=[
                Var(name="interpolant", type="vec3"),
            ],
        ),
        "interpolateAtCentroid(vec4)": Func(
            return_type="vec4",
            name="interpolateAtCentroid",
            args=[
                Var(name="interpolant", type="vec4"),
            ],
        ),
        "interpolateAtOffset(float, vec2)": Func(
            return_type="float",
            name="interpolateAtOffset",
            args=[
                Var(name="interpolant", type="float"),
                Var(name="offset", type="vec2"),
            ],
        ),
        "interpolateAtOffset(vec2, vec2)": Func(
            return_type="vec2",
            name="interpolateAtOffset",
            args=[
                Var(name="interpolant", type="vec2"),
                Var(name="offset", type="vec2"),
            ],
        ),
        "interpolateAtOffset(vec3, vec2)": Func(
            return_type="vec3",
            name="interpolateAtOffset",
            args=[
                Var(name="interpolant", type="vec3"),
                Var(name="offset", type="vec2"),
            ],
        ),
        "interpolateAtOffset(vec4, vec2)": Func(
            return_type="vec4",
            name="interpolateAtOffset",
            args=[
                Var(name="interpolant", type="vec4"),
                Var(name="offset", type="vec2"),
            ],
        ),
        "interpolateAtSample(float, int)": Func(
            return_type="float",
            name="interpolateAtSample",
            args=[
                Var(name="interpolant", type="float"),
                Var(name="sample", type="int"),
            ],
        ),
        "interpolateAtSample(vec2, int)": Func(
            return_type="vec2",
            name="interpolateAtSample",
            args=[
                Var(name="interpolant", type="vec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "interpolateAtSample(vec3, int)": Func(
            return_type="vec3",
            name="interpolateAtSample",
            args=[
                Var(name="interpolant", type="vec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "interpolateAtSample(vec4, int)": Func(
            return_type="vec4",
            name="interpolateAtSample",
            args=[
                Var(name="interpolant", type="vec4"),
                Var(name="sample", type="int"),
            ],
        ),
        "inverse(mat2)": Func(
            return_type="mat2",
            name="inverse",
            args=[
                Var(name="m", type="mat2"),
            ],
        ),
        "inverse(mat3)": Func(
            return_type="mat3",
            name="inverse",
            args=[
                Var(name="m", type="mat3"),
            ],
        ),
        "inverse(mat4)": Func(
            return_type="mat4",
            name="inverse",
            args=[
                Var(name="m", type="mat4"),
            ],
        ),
        "inverse(dmat2)": Func(
            return_type="dmat2",
            name="inverse",
            args=[
                Var(name="m", type="dmat2"),
            ],
        ),
        "inverse(dmat3)": Func(
            return_type="dmat3",
            name="inverse",
            args=[
                Var(name="m", type="dmat3"),
            ],
        ),
        "inverse(dmat4)": Func(
            return_type="dmat4",
            name="inverse",
            args=[
                Var(name="m", type="dmat4"),
            ],
        ),
        "inversesqrt(float)": Func(
            return_type="float",
            name="inversesqrt",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "inversesqrt(vec2)": Func(
            return_type="vec2",
            name="inversesqrt",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "inversesqrt(vec3)": Func(
            return_type="vec3",
            name="inversesqrt",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "inversesqrt(vec4)": Func(
            return_type="vec4",
            name="inversesqrt",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "inversesqrt(double)": Func(
            return_type="double",
            name="inversesqrt",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "inversesqrt(dvec2)": Func(
            return_type="dvec2",
            name="inversesqrt",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "inversesqrt(dvec3)": Func(
            return_type="dvec3",
            name="inversesqrt",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "inversesqrt(dvec4)": Func(
            return_type="dvec4",
            name="inversesqrt",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "isinf(float)": Func(
            return_type="bool",
            name="isinf",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "isinf(vec2)": Func(
            return_type="bvec2",
            name="isinf",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "isinf(vec3)": Func(
            return_type="bvec3",
            name="isinf",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "isinf(vec4)": Func(
            return_type="bvec4",
            name="isinf",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "isinf(double)": Func(
            return_type="bool",
            name="isinf",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "isinf(dvec2)": Func(
            return_type="bvec2",
            name="isinf",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "isinf(dvec3)": Func(
            return_type="bvec3",
            name="isinf",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "isinf(dvec4)": Func(
            return_type="bvec4",
            name="isinf",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "isnan(float)": Func(
            return_type="bool",
            name="isnan",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "isnan(vec2)": Func(
            return_type="bvec2",
            name="isnan",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "isnan(vec3)": Func(
            return_type="bvec3",
            name="isnan",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "isnan(vec4)": Func(
            return_type="bvec4",
            name="isnan",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "isnan(double)": Func(
            return_type="bool",
            name="isnan",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "isnan(dvec2)": Func(
            return_type="bvec2",
            name="isnan",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "isnan(dvec3)": Func(
            return_type="bvec3",
            name="isnan",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "isnan(dvec4)": Func(
            return_type="bvec4",
            name="isnan",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "ldexp(float, int)": Func(
            return_type="float",
            name="ldexp",
            args=[
                Var(name="x", type="float"),
                Var(name="exp", type="int"),
            ],
        ),
        "ldexp(vec2, ivec2)": Func(
            return_type="vec2",
            name="ldexp",
            args=[
                Var(name="x", type="vec2"),
                Var(name="exp", type="ivec2"),
            ],
        ),
        "ldexp(vec3, ivec3)": Func(
            return_type="vec3",
            name="ldexp",
            args=[
                Var(name="x", type="vec3"),
                Var(name="exp", type="ivec3"),
            ],
        ),
        "ldexp(vec4, ivec4)": Func(
            return_type="vec4",
            name="ldexp",
            args=[
                Var(name="x", type="vec4"),
                Var(name="exp", type="ivec4"),
            ],
        ),
        "ldexp(double, int)": Func(
            return_type="double",
            name="ldexp",
            args=[
                Var(name="x", type="double"),
                Var(name="exp", type="int"),
            ],
        ),
        "ldexp(dvec2, ivec2)": Func(
            return_type="dvec2",
            name="ldexp",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="exp", type="ivec2"),
            ],
        ),
        "ldexp(dvec3, ivec3)": Func(
            return_type="dvec3",
            name="ldexp",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="exp", type="ivec3"),
            ],
        ),
        "ldexp(dvec4, ivec4)": Func(
            return_type="dvec4",
            name="ldexp",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="exp", type="ivec4"),
            ],
        ),
        "length(float)": Func(
            return_type="float",
            name="length",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "length(vec2)": Func(
            return_type="float",
            name="length",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "length(vec3)": Func(
            return_type="float",
            name="length",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "length(vec4)": Func(
            return_type="float",
            name="length",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "length(double)": Func(
            return_type="double",
            name="length",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "length(dvec2)": Func(
            return_type="double",
            name="length",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "length(dvec3)": Func(
            return_type="double",
            name="length",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "length(dvec4)": Func(
            return_type="double",
            name="length",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "lessThan(vec2, vec2)": Func(
            return_type="bvec2",
            name="lessThan",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "lessThan(vec3, vec3)": Func(
            return_type="bvec3",
            name="lessThan",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "lessThan(vec4, vec4)": Func(
            return_type="bvec4",
            name="lessThan",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "lessThan(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="lessThan",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "lessThan(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="lessThan",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "lessThan(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="lessThan",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "lessThan(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="lessThan",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "lessThan(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="lessThan",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "lessThan(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="lessThan",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "lessThanEqual(vec2, vec2)": Func(
            return_type="bvec2",
            name="lessThanEqual",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "lessThanEqual(vec3, vec3)": Func(
            return_type="bvec3",
            name="lessThanEqual",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "lessThanEqual(vec4, vec4)": Func(
            return_type="bvec4",
            name="lessThanEqual",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "lessThanEqual(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="lessThanEqual",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "lessThanEqual(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="lessThanEqual",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "lessThanEqual(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="lessThanEqual",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "lessThanEqual(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="lessThanEqual",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "lessThanEqual(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="lessThanEqual",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "lessThanEqual(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="lessThanEqual",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "log(float)": Func(
            return_type="float",
            name="log",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "log(vec2)": Func(
            return_type="vec2",
            name="log",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "log(vec3)": Func(
            return_type="vec3",
            name="log",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "log(vec4)": Func(
            return_type="vec4",
            name="log",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "log2(float)": Func(
            return_type="float",
            name="log2",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "log2(vec2)": Func(
            return_type="vec2",
            name="log2",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "log2(vec3)": Func(
            return_type="vec3",
            name="log2",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "log2(vec4)": Func(
            return_type="vec4",
            name="log2",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "matrixCompMult(mat2, mat2)": Func(
            return_type="mat2",
            name="matrixCompMult",
            args=[
                Var(name="x", type="mat2"),
                Var(name="y", type="mat2"),
            ],
        ),
        "matrixCompMult(mat3, mat3)": Func(
            return_type="mat3",
            name="matrixCompMult",
            args=[
                Var(name="x", type="mat3"),
                Var(name="y", type="mat3"),
            ],
        ),
        "matrixCompMult(mat4, mat4)": Func(
            return_type="mat4",
            name="matrixCompMult",
            args=[
                Var(name="x", type="mat4"),
                Var(name="y", type="mat4"),
            ],
        ),
        "matrixCompMult(dmat2, dmat2)": Func(
            return_type="dmat2",
            name="matrixCompMult",
            args=[
                Var(name="x", type="dmat2"),
                Var(name="y", type="dmat2"),
            ],
        ),
        "matrixCompMult(dmat3, dmat3)": Func(
            return_type="dmat3",
            name="matrixCompMult",
            args=[
                Var(name="x", type="dmat3"),
                Var(name="y", type="dmat3"),
            ],
        ),
        "matrixCompMult(dmat4, dmat4)": Func(
            return_type="dmat4",
            name="matrixCompMult",
            args=[
                Var(name="x", type="dmat4"),
                Var(name="y", type="dmat4"),
            ],
        ),
        "max(float, float)": Func(
            return_type="float",
            name="max",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
            ],
        ),
        "max(vec2, vec2)": Func(
            return_type="vec2",
            name="max",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "max(vec3, vec3)": Func(
            return_type="vec3",
            name="max",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "max(vec4, vec4)": Func(
            return_type="vec4",
            name="max",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "max(vec2, float)": Func(
            return_type="vec2",
            name="max",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="float"),
            ],
        ),
        "max(vec3, float)": Func(
            return_type="vec3",
            name="max",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="float"),
            ],
        ),
        "max(vec4, float)": Func(
            return_type="vec4",
            name="max",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="float"),
            ],
        ),
        "max(double, double)": Func(
            return_type="double",
            name="max",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
            ],
        ),
        "max(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="max",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
            ],
        ),
        "max(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="max",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
            ],
        ),
        "max(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="max",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
            ],
        ),
        "max(dvec2, double)": Func(
            return_type="dvec2",
            name="max",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="double"),
            ],
        ),
        "max(dvec3, double)": Func(
            return_type="dvec3",
            name="max",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="double"),
            ],
        ),
        "max(dvec4, double)": Func(
            return_type="dvec4",
            name="max",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="double"),
            ],
        ),
        "max(int, int)": Func(
            return_type="int",
            name="max",
            args=[
                Var(name="x", type="int"),
                Var(name="y", type="int"),
            ],
        ),
        "max(ivec2, ivec2)": Func(
            return_type="ivec2",
            name="max",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "max(ivec3, ivec3)": Func(
            return_type="ivec3",
            name="max",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "max(ivec4, ivec4)": Func(
            return_type="ivec4",
            name="max",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "max(ivec2, int)": Func(
            return_type="ivec2",
            name="max",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="int"),
            ],
        ),
        "max(ivec3, int)": Func(
            return_type="ivec3",
            name="max",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="int"),
            ],
        ),
        "max(ivec4, int)": Func(
            return_type="ivec4",
            name="max",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="int"),
            ],
        ),
        "max(uint, uint)": Func(
            return_type="uint",
            name="max",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
            ],
        ),
        "max(uvec2, uvec2)": Func(
            return_type="uvec2",
            name="max",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "max(uvec3, uvec3)": Func(
            return_type="uvec3",
            name="max",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "max(uvec4, uvec4)": Func(
            return_type="uvec4",
            name="max",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "max(uvec2, uint)": Func(
            return_type="uvec2",
            name="max",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uint"),
            ],
        ),
        "max(uvec3, uint)": Func(
            return_type="uvec3",
            name="max",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uint"),
            ],
        ),
        "max(uvec4, uint)": Func(
            return_type="uvec4",
            name="max",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uint"),
            ],
        ),
        "memoryBarrier()": Func(return_type="void", name="memoryBarrier", args=[]),
        "memoryBarrierAtomicCounter()": Func(
            return_type="void", name="memoryBarrierAtomicCounter", args=[]
        ),
        "memoryBarrierBuffer()": Func(
            return_type="void", name="memoryBarrierBuffer", args=[]
        ),
        "memoryBarrierImage()": Func(
            return_type="void", name="memoryBarrierImage", args=[]
        ),
        "memoryBarrierShared()": Func(
            return_type="void", name="memoryBarrierShared", args=[]
        ),
        "min(float, float)": Func(
            return_type="float",
            name="min",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
            ],
        ),
        "min(vec2, vec2)": Func(
            return_type="vec2",
            name="min",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "min(vec3, vec3)": Func(
            return_type="vec3",
            name="min",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "min(vec4, vec4)": Func(
            return_type="vec4",
            name="min",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "min(vec2, float)": Func(
            return_type="vec2",
            name="min",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="float"),
            ],
        ),
        "min(vec3, float)": Func(
            return_type="vec3",
            name="min",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="float"),
            ],
        ),
        "min(vec4, float)": Func(
            return_type="vec4",
            name="min",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="float"),
            ],
        ),
        "min(double, double)": Func(
            return_type="double",
            name="min",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
            ],
        ),
        "min(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="min",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
            ],
        ),
        "min(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="min",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
            ],
        ),
        "min(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="min",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
            ],
        ),
        "min(dvec2, double)": Func(
            return_type="dvec2",
            name="min",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="double"),
            ],
        ),
        "min(dvec3, double)": Func(
            return_type="dvec3",
            name="min",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="double"),
            ],
        ),
        "min(dvec4, double)": Func(
            return_type="dvec4",
            name="min",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="double"),
            ],
        ),
        "min(int, int)": Func(
            return_type="int",
            name="min",
            args=[
                Var(name="x", type="int"),
                Var(name="y", type="int"),
            ],
        ),
        "min(ivec2, ivec2)": Func(
            return_type="ivec2",
            name="min",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "min(ivec3, ivec3)": Func(
            return_type="ivec3",
            name="min",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "min(ivec4, ivec4)": Func(
            return_type="ivec4",
            name="min",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "min(ivec2, int)": Func(
            return_type="ivec2",
            name="min",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="int"),
            ],
        ),
        "min(ivec3, int)": Func(
            return_type="ivec3",
            name="min",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="int"),
            ],
        ),
        "min(ivec4, int)": Func(
            return_type="ivec4",
            name="min",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="int"),
            ],
        ),
        "min(uint, uint)": Func(
            return_type="uint",
            name="min",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
            ],
        ),
        "min(uvec2, uvec2)": Func(
            return_type="uvec2",
            name="min",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "min(uvec3, uvec3)": Func(
            return_type="uvec3",
            name="min",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "min(uvec4, uvec4)": Func(
            return_type="uvec4",
            name="min",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "min(uvec2, uint)": Func(
            return_type="uvec2",
            name="min",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uint"),
            ],
        ),
        "min(uvec3, uint)": Func(
            return_type="uvec3",
            name="min",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uint"),
            ],
        ),
        "min(uvec4, uint)": Func(
            return_type="uvec4",
            name="min",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uint"),
            ],
        ),
        "mix(float, float, float)": Func(
            return_type="float",
            name="mix",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
                Var(name="a", type="float"),
            ],
        ),
        "mix(vec2, vec2, vec2)": Func(
            return_type="vec2",
            name="mix",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
                Var(name="a", type="vec2"),
            ],
        ),
        "mix(vec3, vec3, vec3)": Func(
            return_type="vec3",
            name="mix",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
                Var(name="a", type="vec3"),
            ],
        ),
        "mix(vec4, vec4, vec4)": Func(
            return_type="vec4",
            name="mix",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
                Var(name="a", type="vec4"),
            ],
        ),
        "mix(vec2, vec2, float)": Func(
            return_type="vec2",
            name="mix",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
                Var(name="a", type="float"),
            ],
        ),
        "mix(vec3, vec3, float)": Func(
            return_type="vec3",
            name="mix",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
                Var(name="a", type="float"),
            ],
        ),
        "mix(vec4, vec4, float)": Func(
            return_type="vec4",
            name="mix",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
                Var(name="a", type="float"),
            ],
        ),
        "mix(double, double, double)": Func(
            return_type="double",
            name="mix",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
                Var(name="a", type="double"),
            ],
        ),
        "mix(dvec2, dvec2, dvec2)": Func(
            return_type="dvec2",
            name="mix",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
                Var(name="a", type="dvec2"),
            ],
        ),
        "mix(dvec3, dvec3, dvec3)": Func(
            return_type="dvec3",
            name="mix",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
                Var(name="a", type="dvec3"),
            ],
        ),
        "mix(dvec4, dvec4, dvec4)": Func(
            return_type="dvec4",
            name="mix",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
                Var(name="a", type="dvec4"),
            ],
        ),
        "mix(dvec2, dvec2, double)": Func(
            return_type="dvec2",
            name="mix",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
                Var(name="a", type="double"),
            ],
        ),
        "mix(dvec3, dvec3, double)": Func(
            return_type="dvec3",
            name="mix",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
                Var(name="a", type="double"),
            ],
        ),
        "mix(dvec4, dvec4, double)": Func(
            return_type="dvec4",
            name="mix",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
                Var(name="a", type="double"),
            ],
        ),
        "mix(float, float, bool)": Func(
            return_type="float",
            name="mix",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
                Var(name="a", type="bool"),
            ],
        ),
        "mix(vec2, vec2, bvec2)": Func(
            return_type="vec2",
            name="mix",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
                Var(name="a", type="bvec2"),
            ],
        ),
        "mix(vec3, vec3, bvec3)": Func(
            return_type="vec3",
            name="mix",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
                Var(name="a", type="bvec3"),
            ],
        ),
        "mix(vec4, vec4, bvec4)": Func(
            return_type="vec4",
            name="mix",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
                Var(name="a", type="bvec4"),
            ],
        ),
        "mix(double, double, bool)": Func(
            return_type="double",
            name="mix",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
                Var(name="a", type="bool"),
            ],
        ),
        "mix(dvec2, dvec2, bvec2)": Func(
            return_type="dvec2",
            name="mix",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
                Var(name="a", type="bvec2"),
            ],
        ),
        "mix(dvec3, dvec3, bvec3)": Func(
            return_type="dvec3",
            name="mix",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
                Var(name="a", type="bvec3"),
            ],
        ),
        "mix(dvec4, dvec4, bvec4)": Func(
            return_type="dvec4",
            name="mix",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
                Var(name="a", type="bvec4"),
            ],
        ),
        "mix(int, int, bool)": Func(
            return_type="int",
            name="mix",
            args=[
                Var(name="x", type="int"),
                Var(name="y", type="int"),
                Var(name="a", type="bool"),
            ],
        ),
        "mix(ivec2, ivec2, bvec2)": Func(
            return_type="ivec2",
            name="mix",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
                Var(name="a", type="bvec2"),
            ],
        ),
        "mix(ivec3, ivec3, bvec3)": Func(
            return_type="ivec3",
            name="mix",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
                Var(name="a", type="bvec3"),
            ],
        ),
        "mix(ivec4, ivec4, bvec4)": Func(
            return_type="ivec4",
            name="mix",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
                Var(name="a", type="bvec4"),
            ],
        ),
        "mix(uint, uint, bool)": Func(
            return_type="uint",
            name="mix",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
                Var(name="a", type="bool"),
            ],
        ),
        "mix(uvec2, uvec2, bvec2)": Func(
            return_type="uvec2",
            name="mix",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
                Var(name="a", type="bvec2"),
            ],
        ),
        "mix(uvec3, uvec3, bvec3)": Func(
            return_type="uvec3",
            name="mix",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
                Var(name="a", type="bvec3"),
            ],
        ),
        "mix(uvec4, uvec4, bvec4)": Func(
            return_type="uvec4",
            name="mix",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
                Var(name="a", type="bvec4"),
            ],
        ),
        "mix(bool, bool, bool)": Func(
            return_type="bool",
            name="mix",
            args=[
                Var(name="x", type="bool"),
                Var(name="y", type="bool"),
                Var(name="a", type="bool"),
            ],
        ),
        "mix(bvec2, bvec2, bvec2)": Func(
            return_type="bvec2",
            name="mix",
            args=[
                Var(name="x", type="bvec2"),
                Var(name="y", type="bvec2"),
                Var(name="a", type="bvec2"),
            ],
        ),
        "mix(bvec3, bvec3, bvec3)": Func(
            return_type="bvec3",
            name="mix",
            args=[
                Var(name="x", type="bvec3"),
                Var(name="y", type="bvec3"),
                Var(name="a", type="bvec3"),
            ],
        ),
        "mix(bvec4, bvec4, bvec4)": Func(
            return_type="bvec4",
            name="mix",
            args=[
                Var(name="x", type="bvec4"),
                Var(name="y", type="bvec4"),
                Var(name="a", type="bvec4"),
            ],
        ),
        "mod(float, float)": Func(
            return_type="float",
            name="mod",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
            ],
        ),
        "mod(vec2, float)": Func(
            return_type="vec2",
            name="mod",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="float"),
            ],
        ),
        "mod(vec3, float)": Func(
            return_type="vec3",
            name="mod",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="float"),
            ],
        ),
        "mod(vec4, float)": Func(
            return_type="vec4",
            name="mod",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="float"),
            ],
        ),
        "mod(vec2, vec2)": Func(
            return_type="vec2",
            name="mod",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "mod(vec3, vec3)": Func(
            return_type="vec3",
            name="mod",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "mod(vec4, vec4)": Func(
            return_type="vec4",
            name="mod",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "mod(double, double)": Func(
            return_type="double",
            name="mod",
            args=[
                Var(name="x", type="double"),
                Var(name="y", type="double"),
            ],
        ),
        "mod(dvec2, double)": Func(
            return_type="dvec2",
            name="mod",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="double"),
            ],
        ),
        "mod(dvec3, double)": Func(
            return_type="dvec3",
            name="mod",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="double"),
            ],
        ),
        "mod(dvec4, double)": Func(
            return_type="dvec4",
            name="mod",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="double"),
            ],
        ),
        "mod(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="mod",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="y", type="dvec2"),
            ],
        ),
        "mod(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="mod",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="y", type="dvec3"),
            ],
        ),
        "mod(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="mod",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="y", type="dvec4"),
            ],
        ),
        "modf(float, float)": Func(
            return_type="float",
            name="modf",
            args=[
                Var(name="x", type="float"),
                Var(name="i", type="float"),
            ],
        ),
        "modf(vec2, vec2)": Func(
            return_type="vec2",
            name="modf",
            args=[
                Var(name="x", type="vec2"),
                Var(name="i", type="vec2"),
            ],
        ),
        "modf(vec3, vec3)": Func(
            return_type="vec3",
            name="modf",
            args=[
                Var(name="x", type="vec3"),
                Var(name="i", type="vec3"),
            ],
        ),
        "modf(vec4, vec4)": Func(
            return_type="vec4",
            name="modf",
            args=[
                Var(name="x", type="vec4"),
                Var(name="i", type="vec4"),
            ],
        ),
        "modf(double, double)": Func(
            return_type="double",
            name="modf",
            args=[
                Var(name="x", type="double"),
                Var(name="i", type="double"),
            ],
        ),
        "modf(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="modf",
            args=[
                Var(name="x", type="dvec2"),
                Var(name="i", type="dvec2"),
            ],
        ),
        "modf(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="modf",
            args=[
                Var(name="x", type="dvec3"),
                Var(name="i", type="dvec3"),
            ],
        ),
        "modf(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="modf",
            args=[
                Var(name="x", type="dvec4"),
                Var(name="i", type="dvec4"),
            ],
        ),
        "noise1(float)": Func(
            return_type="float",
            name="noise1",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "noise1(vec2)": Func(
            return_type="float",
            name="noise1",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "noise1(vec3)": Func(
            return_type="float",
            name="noise1",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "noise1(vec4)": Func(
            return_type="float",
            name="noise1",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "noise2(float)": Func(
            return_type="vec2",
            name="noise2",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "noise2(vec2)": Func(
            return_type="vec2",
            name="noise2",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "noise2(vec3)": Func(
            return_type="vec2",
            name="noise2",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "noise2(vec4)": Func(
            return_type="vec2",
            name="noise2",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "noise3(float)": Func(
            return_type="vec3",
            name="noise3",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "noise3(vec2)": Func(
            return_type="vec3",
            name="noise3",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "noise3(vec3)": Func(
            return_type="vec3",
            name="noise3",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "noise3(vec4)": Func(
            return_type="vec3",
            name="noise3",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "noise4(float)": Func(
            return_type="vec4",
            name="noise4",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "noise4(vec2)": Func(
            return_type="vec4",
            name="noise4",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "noise4(vec3)": Func(
            return_type="vec4",
            name="noise4",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "noise4(vec4)": Func(
            return_type="vec4",
            name="noise4",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "normalize(float)": Func(
            return_type="float",
            name="normalize",
            args=[
                Var(name="v", type="float"),
            ],
        ),
        "normalize(vec2)": Func(
            return_type="vec2",
            name="normalize",
            args=[
                Var(name="v", type="vec2"),
            ],
        ),
        "normalize(vec3)": Func(
            return_type="vec3",
            name="normalize",
            args=[
                Var(name="v", type="vec3"),
            ],
        ),
        "normalize(vec4)": Func(
            return_type="vec4",
            name="normalize",
            args=[
                Var(name="v", type="vec4"),
            ],
        ),
        "normalize(double)": Func(
            return_type="double",
            name="normalize",
            args=[
                Var(name="v", type="double"),
            ],
        ),
        "normalize(dvec2)": Func(
            return_type="dvec2",
            name="normalize",
            args=[
                Var(name="v", type="dvec2"),
            ],
        ),
        "normalize(dvec3)": Func(
            return_type="dvec3",
            name="normalize",
            args=[
                Var(name="v", type="dvec3"),
            ],
        ),
        "normalize(dvec4)": Func(
            return_type="dvec4",
            name="normalize",
            args=[
                Var(name="v", type="dvec4"),
            ],
        ),
        "not(bvec2)": Func(
            return_type="bvec2",
            name="not",
            args=[
                Var(name="x", type="bvec2"),
            ],
        ),
        "not(bvec3)": Func(
            return_type="bvec3",
            name="not",
            args=[
                Var(name="x", type="bvec3"),
            ],
        ),
        "not(bvec4)": Func(
            return_type="bvec4",
            name="not",
            args=[
                Var(name="x", type="bvec4"),
            ],
        ),
        "notEqual(vec2, vec2)": Func(
            return_type="bvec2",
            name="notEqual",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "notEqual(vec3, vec3)": Func(
            return_type="bvec3",
            name="notEqual",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "notEqual(vec4, vec4)": Func(
            return_type="bvec4",
            name="notEqual",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "notEqual(ivec2, ivec2)": Func(
            return_type="bvec2",
            name="notEqual",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
            ],
        ),
        "notEqual(ivec3, ivec3)": Func(
            return_type="bvec3",
            name="notEqual",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
            ],
        ),
        "notEqual(ivec4, ivec4)": Func(
            return_type="bvec4",
            name="notEqual",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
            ],
        ),
        "notEqual(uvec2, uvec2)": Func(
            return_type="bvec2",
            name="notEqual",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
            ],
        ),
        "notEqual(uvec3, uvec3)": Func(
            return_type="bvec3",
            name="notEqual",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
            ],
        ),
        "notEqual(uvec4, uvec4)": Func(
            return_type="bvec4",
            name="notEqual",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
            ],
        ),
        "outerProduct(vec2, vec2)": Func(
            return_type="mat2",
            name="outerProduct",
            args=[
                Var(name="c", type="vec2"),
                Var(name="r", type="vec2"),
            ],
        ),
        "outerProduct(vec3, vec3)": Func(
            return_type="mat3",
            name="outerProduct",
            args=[
                Var(name="c", type="vec3"),
                Var(name="r", type="vec3"),
            ],
        ),
        "outerProduct(vec4, vec4)": Func(
            return_type="mat4",
            name="outerProduct",
            args=[
                Var(name="c", type="vec4"),
                Var(name="r", type="vec4"),
            ],
        ),
        "outerProduct(vec3, vec2)": Func(
            return_type="mat2x3",
            name="outerProduct",
            args=[
                Var(name="c", type="vec3"),
                Var(name="r", type="vec2"),
            ],
        ),
        "outerProduct(vec2, vec3)": Func(
            return_type="mat3x2",
            name="outerProduct",
            args=[
                Var(name="c", type="vec2"),
                Var(name="r", type="vec3"),
            ],
        ),
        "outerProduct(vec4, vec2)": Func(
            return_type="mat2x4",
            name="outerProduct",
            args=[
                Var(name="c", type="vec4"),
                Var(name="r", type="vec2"),
            ],
        ),
        "outerProduct(vec2, vec4)": Func(
            return_type="mat4x2",
            name="outerProduct",
            args=[
                Var(name="c", type="vec2"),
                Var(name="r", type="vec4"),
            ],
        ),
        "outerProduct(vec4, vec3)": Func(
            return_type="mat3x4",
            name="outerProduct",
            args=[
                Var(name="c", type="vec4"),
                Var(name="r", type="vec3"),
            ],
        ),
        "outerProduct(vec3, vec4)": Func(
            return_type="mat4x3",
            name="outerProduct",
            args=[
                Var(name="c", type="vec3"),
                Var(name="r", type="vec4"),
            ],
        ),
        "outerProduct(dvec2, dvec2)": Func(
            return_type="dmat2",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec2"),
                Var(name="r", type="dvec2"),
            ],
        ),
        "outerProduct(dvec3, dvec3)": Func(
            return_type="dmat3",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec3"),
                Var(name="r", type="dvec3"),
            ],
        ),
        "outerProduct(dvec4, dvec4)": Func(
            return_type="dmat4",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec4"),
                Var(name="r", type="dvec4"),
            ],
        ),
        "outerProduct(dvec3, dvec2)": Func(
            return_type="dmat2x3",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec3"),
                Var(name="r", type="dvec2"),
            ],
        ),
        "outerProduct(dvec2, dvec3)": Func(
            return_type="dmat3x2",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec2"),
                Var(name="r", type="dvec3"),
            ],
        ),
        "outerProduct(dvec4, dvec2)": Func(
            return_type="dmat2x4",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec4"),
                Var(name="r", type="dvec2"),
            ],
        ),
        "outerProduct(dvec2, dvec4)": Func(
            return_type="dmat4x2",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec2"),
                Var(name="r", type="dvec4"),
            ],
        ),
        "outerProduct(dvec4, dvec3)": Func(
            return_type="dmat3x4",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec4"),
                Var(name="r", type="dvec3"),
            ],
        ),
        "outerProduct(dvec3, dvec4)": Func(
            return_type="dmat4x3",
            name="outerProduct",
            args=[
                Var(name="c", type="dvec3"),
                Var(name="r", type="dvec4"),
            ],
        ),
        "packDouble2x32(uvec2)": Func(
            return_type="double",
            name="packDouble2x32",
            args=[
                Var(name="v", type="uvec2"),
            ],
        ),
        "packHalf2x16(vec2)": Func(
            return_type="uint",
            name="packHalf2x16",
            args=[
                Var(name="v", type="vec2"),
            ],
        ),
        "packUnorm2x16(vec2)": Func(
            return_type="uint",
            name="packUnorm2x16",
            args=[
                Var(name="v", type="vec2"),
            ],
        ),
        "packSnorm2x16(vec2)": Func(
            return_type="uint",
            name="packSnorm2x16",
            args=[
                Var(name="v", type="vec2"),
            ],
        ),
        "packUnorm4x8(vec4)": Func(
            return_type="uint",
            name="packUnorm4x8",
            args=[
                Var(name="v", type="vec4"),
            ],
        ),
        "packSnorm4x8(vec4)": Func(
            return_type="uint",
            name="packSnorm4x8",
            args=[
                Var(name="v", type="vec4"),
            ],
        ),
        "pow(float, float)": Func(
            return_type="float",
            name="pow",
            args=[
                Var(name="x", type="float"),
                Var(name="y", type="float"),
            ],
        ),
        "pow(vec2, vec2)": Func(
            return_type="vec2",
            name="pow",
            args=[
                Var(name="x", type="vec2"),
                Var(name="y", type="vec2"),
            ],
        ),
        "pow(vec3, vec3)": Func(
            return_type="vec3",
            name="pow",
            args=[
                Var(name="x", type="vec3"),
                Var(name="y", type="vec3"),
            ],
        ),
        "pow(vec4, vec4)": Func(
            return_type="vec4",
            name="pow",
            args=[
                Var(name="x", type="vec4"),
                Var(name="y", type="vec4"),
            ],
        ),
        "radians(float)": Func(
            return_type="float",
            name="radians",
            args=[
                Var(name="degrees", type="float"),
            ],
        ),
        "radians(vec2)": Func(
            return_type="vec2",
            name="radians",
            args=[
                Var(name="degrees", type="vec2"),
            ],
        ),
        "radians(vec3)": Func(
            return_type="vec3",
            name="radians",
            args=[
                Var(name="degrees", type="vec3"),
            ],
        ),
        "radians(vec4)": Func(
            return_type="vec4",
            name="radians",
            args=[
                Var(name="degrees", type="vec4"),
            ],
        ),
        "reflect(float, float)": Func(
            return_type="float",
            name="reflect",
            args=[
                Var(name="I", type="float"),
                Var(name="N", type="float"),
            ],
        ),
        "reflect(vec2, vec2)": Func(
            return_type="vec2",
            name="reflect",
            args=[
                Var(name="I", type="vec2"),
                Var(name="N", type="vec2"),
            ],
        ),
        "reflect(vec3, vec3)": Func(
            return_type="vec3",
            name="reflect",
            args=[
                Var(name="I", type="vec3"),
                Var(name="N", type="vec3"),
            ],
        ),
        "reflect(vec4, vec4)": Func(
            return_type="vec4",
            name="reflect",
            args=[
                Var(name="I", type="vec4"),
                Var(name="N", type="vec4"),
            ],
        ),
        "reflect(double, double)": Func(
            return_type="double",
            name="reflect",
            args=[
                Var(name="I", type="double"),
                Var(name="N", type="double"),
            ],
        ),
        "reflect(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="reflect",
            args=[
                Var(name="I", type="dvec2"),
                Var(name="N", type="dvec2"),
            ],
        ),
        "reflect(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="reflect",
            args=[
                Var(name="I", type="dvec3"),
                Var(name="N", type="dvec3"),
            ],
        ),
        "reflect(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="reflect",
            args=[
                Var(name="I", type="dvec4"),
                Var(name="N", type="dvec4"),
            ],
        ),
        "refract(float, float, float)": Func(
            return_type="float",
            name="refract",
            args=[
                Var(name="I", type="float"),
                Var(name="N", type="float"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(vec2, vec2, float)": Func(
            return_type="vec2",
            name="refract",
            args=[
                Var(name="I", type="vec2"),
                Var(name="N", type="vec2"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(vec3, vec3, float)": Func(
            return_type="vec3",
            name="refract",
            args=[
                Var(name="I", type="vec3"),
                Var(name="N", type="vec3"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(vec4, vec4, float)": Func(
            return_type="vec4",
            name="refract",
            args=[
                Var(name="I", type="vec4"),
                Var(name="N", type="vec4"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(double, double, float)": Func(
            return_type="double",
            name="refract",
            args=[
                Var(name="I", type="double"),
                Var(name="N", type="double"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(dvec2, dvec2, float)": Func(
            return_type="dvec2",
            name="refract",
            args=[
                Var(name="I", type="dvec2"),
                Var(name="N", type="dvec2"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(dvec3, dvec3, float)": Func(
            return_type="dvec3",
            name="refract",
            args=[
                Var(name="I", type="dvec3"),
                Var(name="N", type="dvec3"),
                Var(name="eta", type="float"),
            ],
        ),
        "refract(dvec4, dvec4, float)": Func(
            return_type="dvec4",
            name="refract",
            args=[
                Var(name="I", type="dvec4"),
                Var(name="N", type="dvec4"),
                Var(name="eta", type="float"),
            ],
        ),
        "round(float)": Func(
            return_type="float",
            name="round",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "round(vec2)": Func(
            return_type="vec2",
            name="round",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "round(vec3)": Func(
            return_type="vec3",
            name="round",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "round(vec4)": Func(
            return_type="vec4",
            name="round",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "round(double)": Func(
            return_type="double",
            name="round",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "round(dvec2)": Func(
            return_type="dvec2",
            name="round",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "round(dvec3)": Func(
            return_type="dvec3",
            name="round",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "round(dvec4)": Func(
            return_type="dvec4",
            name="round",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "roundEven(float)": Func(
            return_type="float",
            name="roundEven",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "roundEven(vec2)": Func(
            return_type="vec2",
            name="roundEven",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "roundEven(vec3)": Func(
            return_type="vec3",
            name="roundEven",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "roundEven(vec4)": Func(
            return_type="vec4",
            name="roundEven",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "roundEven(double)": Func(
            return_type="double",
            name="roundEven",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "roundEven(dvec2)": Func(
            return_type="dvec2",
            name="roundEven",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "roundEven(dvec3)": Func(
            return_type="dvec3",
            name="roundEven",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "roundEven(dvec4)": Func(
            return_type="dvec4",
            name="roundEven",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "sign(float)": Func(
            return_type="float",
            name="sign",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "sign(vec2)": Func(
            return_type="vec2",
            name="sign",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "sign(vec3)": Func(
            return_type="vec3",
            name="sign",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "sign(vec4)": Func(
            return_type="vec4",
            name="sign",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "sign(int)": Func(
            return_type="int",
            name="sign",
            args=[
                Var(name="x", type="int"),
            ],
        ),
        "sign(ivec2)": Func(
            return_type="ivec2",
            name="sign",
            args=[
                Var(name="x", type="ivec2"),
            ],
        ),
        "sign(ivec3)": Func(
            return_type="ivec3",
            name="sign",
            args=[
                Var(name="x", type="ivec3"),
            ],
        ),
        "sign(ivec4)": Func(
            return_type="ivec4",
            name="sign",
            args=[
                Var(name="x", type="ivec4"),
            ],
        ),
        "sign(double)": Func(
            return_type="double",
            name="sign",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "sign(dvec2)": Func(
            return_type="dvec2",
            name="sign",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "sign(dvec3)": Func(
            return_type="dvec3",
            name="sign",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "sign(dvec4)": Func(
            return_type="dvec4",
            name="sign",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "sin(float)": Func(
            return_type="float",
            name="sin",
            args=[
                Var(name="angle", type="float"),
            ],
        ),
        "sin(vec2)": Func(
            return_type="vec2",
            name="sin",
            args=[
                Var(name="angle", type="vec2"),
            ],
        ),
        "sin(vec3)": Func(
            return_type="vec3",
            name="sin",
            args=[
                Var(name="angle", type="vec3"),
            ],
        ),
        "sin(vec4)": Func(
            return_type="vec4",
            name="sin",
            args=[
                Var(name="angle", type="vec4"),
            ],
        ),
        "sinh(float)": Func(
            return_type="float",
            name="sinh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "sinh(vec2)": Func(
            return_type="vec2",
            name="sinh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "sinh(vec3)": Func(
            return_type="vec3",
            name="sinh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "sinh(vec4)": Func(
            return_type="vec4",
            name="sinh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "smoothstep(float, float, float)": Func(
            return_type="float",
            name="smoothstep",
            args=[
                Var(name="edge0", type="float"),
                Var(name="edge1", type="float"),
                Var(name="x", type="float"),
            ],
        ),
        "smoothstep(vec2, vec2, vec2)": Func(
            return_type="vec2",
            name="smoothstep",
            args=[
                Var(name="edge0", type="vec2"),
                Var(name="edge1", type="vec2"),
                Var(name="x", type="vec2"),
            ],
        ),
        "smoothstep(vec3, vec3, vec3)": Func(
            return_type="vec3",
            name="smoothstep",
            args=[
                Var(name="edge0", type="vec3"),
                Var(name="edge1", type="vec3"),
                Var(name="x", type="vec3"),
            ],
        ),
        "smoothstep(vec4, vec4, vec4)": Func(
            return_type="vec4",
            name="smoothstep",
            args=[
                Var(name="edge0", type="vec4"),
                Var(name="edge1", type="vec4"),
                Var(name="x", type="vec4"),
            ],
        ),
        "smoothstep(float, float, vec2)": Func(
            return_type="vec2",
            name="smoothstep",
            args=[
                Var(name="edge0", type="float"),
                Var(name="edge1", type="float"),
                Var(name="x", type="vec2"),
            ],
        ),
        "smoothstep(float, float, vec3)": Func(
            return_type="vec3",
            name="smoothstep",
            args=[
                Var(name="edge0", type="float"),
                Var(name="edge1", type="float"),
                Var(name="x", type="vec3"),
            ],
        ),
        "smoothstep(float, float, vec4)": Func(
            return_type="vec4",
            name="smoothstep",
            args=[
                Var(name="edge0", type="float"),
                Var(name="edge1", type="float"),
                Var(name="x", type="vec4"),
            ],
        ),
        "smoothstep(double, double, double)": Func(
            return_type="double",
            name="smoothstep",
            args=[
                Var(name="edge0", type="double"),
                Var(name="edge1", type="double"),
                Var(name="x", type="double"),
            ],
        ),
        "smoothstep(dvec2, dvec2, dvec2)": Func(
            return_type="dvec2",
            name="smoothstep",
            args=[
                Var(name="edge0", type="dvec2"),
                Var(name="edge1", type="dvec2"),
                Var(name="x", type="dvec2"),
            ],
        ),
        "smoothstep(dvec3, dvec3, dvec3)": Func(
            return_type="dvec3",
            name="smoothstep",
            args=[
                Var(name="edge0", type="dvec3"),
                Var(name="edge1", type="dvec3"),
                Var(name="x", type="dvec3"),
            ],
        ),
        "smoothstep(dvec4, dvec4, dvec4)": Func(
            return_type="dvec4",
            name="smoothstep",
            args=[
                Var(name="edge0", type="dvec4"),
                Var(name="edge1", type="dvec4"),
                Var(name="x", type="dvec4"),
            ],
        ),
        "smoothstep(double, double, dvec2)": Func(
            return_type="dvec2",
            name="smoothstep",
            args=[
                Var(name="edge0", type="double"),
                Var(name="edge1", type="double"),
                Var(name="x", type="dvec2"),
            ],
        ),
        "smoothstep(double, double, dvec3)": Func(
            return_type="dvec3",
            name="smoothstep",
            args=[
                Var(name="edge0", type="double"),
                Var(name="edge1", type="double"),
                Var(name="x", type="dvec3"),
            ],
        ),
        "smoothstep(double, double, dvec4)": Func(
            return_type="dvec4",
            name="smoothstep",
            args=[
                Var(name="edge0", type="double"),
                Var(name="edge1", type="double"),
                Var(name="x", type="dvec4"),
            ],
        ),
        "sqrt(float)": Func(
            return_type="float",
            name="sqrt",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "sqrt(vec2)": Func(
            return_type="vec2",
            name="sqrt",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "sqrt(vec3)": Func(
            return_type="vec3",
            name="sqrt",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "sqrt(vec4)": Func(
            return_type="vec4",
            name="sqrt",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "sqrt(double)": Func(
            return_type="double",
            name="sqrt",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "sqrt(dvec2)": Func(
            return_type="dvec2",
            name="sqrt",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "sqrt(dvec3)": Func(
            return_type="dvec3",
            name="sqrt",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "sqrt(dvec4)": Func(
            return_type="dvec4",
            name="sqrt",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "step(float, float)": Func(
            return_type="float",
            name="step",
            args=[
                Var(name="edge", type="float"),
                Var(name="x", type="float"),
            ],
        ),
        "step(vec2, vec2)": Func(
            return_type="vec2",
            name="step",
            args=[
                Var(name="edge", type="vec2"),
                Var(name="x", type="vec2"),
            ],
        ),
        "step(vec3, vec3)": Func(
            return_type="vec3",
            name="step",
            args=[
                Var(name="edge", type="vec3"),
                Var(name="x", type="vec3"),
            ],
        ),
        "step(vec4, vec4)": Func(
            return_type="vec4",
            name="step",
            args=[
                Var(name="edge", type="vec4"),
                Var(name="x", type="vec4"),
            ],
        ),
        "step(float, vec2)": Func(
            return_type="vec2",
            name="step",
            args=[
                Var(name="edge", type="float"),
                Var(name="x", type="vec2"),
            ],
        ),
        "step(float, vec3)": Func(
            return_type="vec3",
            name="step",
            args=[
                Var(name="edge", type="float"),
                Var(name="x", type="vec3"),
            ],
        ),
        "step(float, vec4)": Func(
            return_type="vec4",
            name="step",
            args=[
                Var(name="edge", type="float"),
                Var(name="x", type="vec4"),
            ],
        ),
        "step(double, double)": Func(
            return_type="double",
            name="step",
            args=[
                Var(name="edge", type="double"),
                Var(name="x", type="double"),
            ],
        ),
        "step(dvec2, dvec2)": Func(
            return_type="dvec2",
            name="step",
            args=[
                Var(name="edge", type="dvec2"),
                Var(name="x", type="dvec2"),
            ],
        ),
        "step(dvec3, dvec3)": Func(
            return_type="dvec3",
            name="step",
            args=[
                Var(name="edge", type="dvec3"),
                Var(name="x", type="dvec3"),
            ],
        ),
        "step(dvec4, dvec4)": Func(
            return_type="dvec4",
            name="step",
            args=[
                Var(name="edge", type="dvec4"),
                Var(name="x", type="dvec4"),
            ],
        ),
        "step(double, dvec2)": Func(
            return_type="dvec2",
            name="step",
            args=[
                Var(name="edge", type="double"),
                Var(name="x", type="dvec2"),
            ],
        ),
        "step(double, dvec3)": Func(
            return_type="dvec3",
            name="step",
            args=[
                Var(name="edge", type="double"),
                Var(name="x", type="dvec3"),
            ],
        ),
        "step(double, dvec4)": Func(
            return_type="dvec4",
            name="step",
            args=[
                Var(name="edge", type="double"),
                Var(name="x", type="dvec4"),
            ],
        ),
        "tan(float)": Func(
            return_type="float",
            name="tan",
            args=[
                Var(name="angle", type="float"),
            ],
        ),
        "tan(vec2)": Func(
            return_type="vec2",
            name="tan",
            args=[
                Var(name="angle", type="vec2"),
            ],
        ),
        "tan(vec3)": Func(
            return_type="vec3",
            name="tan",
            args=[
                Var(name="angle", type="vec3"),
            ],
        ),
        "tan(vec4)": Func(
            return_type="vec4",
            name="tan",
            args=[
                Var(name="angle", type="vec4"),
            ],
        ),
        "tanh(float)": Func(
            return_type="float",
            name="tanh",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "tanh(vec2)": Func(
            return_type="vec2",
            name="tanh",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "tanh(vec3)": Func(
            return_type="vec3",
            name="tanh",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "tanh(vec4)": Func(
            return_type="vec4",
            name="tanh",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "texelFetch(sampler1D, int, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(isampler1D, int, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(usampler1D, int, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(sampler2D, ivec2, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(isampler2D, ivec2, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(usampler2D, ivec2, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(sampler3D, ivec3, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(isampler3D, ivec3, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(usampler3D, ivec3, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(sampler2DRect, ivec2)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "texelFetch(isampler2DRect, ivec2)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "texelFetch(usampler2DRect, ivec2)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="ivec2"),
            ],
        ),
        "texelFetch(sampler1DArray, ivec2, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(isampler1DArray, ivec2, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(usampler1DArray, ivec2, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(sampler2DArray, ivec3, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(isampler2DArray, ivec3, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(usampler2DArray, ivec3, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
            ],
        ),
        "texelFetch(samplerBuffer, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="samplerBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "texelFetch(isamplerBuffer, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isamplerBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "texelFetch(usamplerBuffer, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usamplerBuffer"),
                Var(name="P", type="int"),
            ],
        ),
        "texelFetch(sampler2DMS, ivec2, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetch(isampler2DMS, ivec2, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetch(usampler2DMS, ivec2, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler2DMS"),
                Var(name="P", type="ivec2"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetch(sampler2DMSArray, ivec3, int)": Func(
            return_type="vec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="sampler2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetch(isampler2DMSArray, ivec3, int)": Func(
            return_type="ivec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="isampler2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetch(usampler2DMSArray, ivec3, int)": Func(
            return_type="uvec4",
            name="texelFetch",
            args=[
                Var(name="sampler", type="usampler2DMSArray"),
                Var(name="P", type="ivec3"),
                Var(name="sample", type="int"),
            ],
        ),
        "texelFetchOffset(sampler1D, int, int, int)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
                Var(name="offset", type="int"),
            ],
        ),
        "texelFetchOffset(isampler1D, int, int, int)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
                Var(name="offset", type="int"),
            ],
        ),
        "texelFetchOffset(usampler1D, int, int, int)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="int"),
                Var(name="lod", type="int"),
                Var(name="offset", type="int"),
            ],
        ),
        "texelFetchOffset(sampler2D, ivec2, int, ivec2)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(isampler2D, ivec2, int, ivec2)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(usampler2D, ivec2, int, ivec2)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(sampler3D, ivec3, int, ivec3)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "texelFetchOffset(isampler3D, ivec3, int, ivec3)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "texelFetchOffset(usampler3D, ivec3, int, ivec3)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "texelFetchOffset(sampler2DRect, ivec2, ivec2)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(isampler2DRect, ivec2, ivec2)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(usampler2DRect, ivec2, ivec2)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="ivec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(sampler1DArray, ivec2, int, ivec2)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(isampler1DArray, ivec2, int, ivec2)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(usampler1DArray, ivec2, int, ivec2)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="ivec2"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(sampler2DArray, ivec3, int, ivec2)": Func(
            return_type="vec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(isampler2DArray, ivec3, int, ivec2)": Func(
            return_type="ivec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texelFetchOffset(usampler2DArray, ivec3, int, ivec2)": Func(
            return_type="uvec4",
            name="texelFetchOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="ivec3"),
                Var(name="lod", type="int"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "texture(sampler1D, float, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler1D, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "texture(isampler1D, float, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isampler1D, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "texture(usampler1D, float, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usampler1D, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "texture(sampler2D, vec2, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler2D, vec2)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(isampler2D, vec2, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isampler2D, vec2)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(usampler2D, vec2, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usampler2D, vec2)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(sampler3D, vec3, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler3D, vec3)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(isampler3D, vec3, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isampler3D, vec3)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(usampler3D, vec3, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usampler3D, vec3)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(samplerCube, vec3, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(samplerCube, vec3)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(isamplerCube, vec3, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isamplerCube, vec3)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(usamplerCube, vec3, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usamplerCube, vec3)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(sampler1DShadow, vec3, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler1DShadow, vec3)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(sampler2DShadow, vec3, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler2DShadow, vec3)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(samplerCubeShadow, vec4, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(samplerCubeShadow, vec4)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="P", type="vec4"),
            ],
        ),
        "texture(sampler1DArray, vec2, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler1DArray, vec2)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(isampler1DArray, vec2, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isampler1DArray, vec2)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(usampler1DArray, vec2, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usampler1DArray, vec2)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(sampler2DArray, vec3, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler2DArray, vec3)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(isampler2DArray, vec3, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isampler2DArray, vec3)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(usampler2DArray, vec3, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usampler2DArray, vec3)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(samplerCubeArray, vec4, float)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(samplerCubeArray, vec4)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "texture(isamplerCubeArray, vec4, float)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(isamplerCubeArray, vec4)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "texture(usamplerCubeArray, vec4, float)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(usamplerCubeArray, vec4)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "texture(sampler1DArrayShadow, vec3, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler1DArrayShadow, vec3)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(sampler2DArrayShadow, vec4, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "texture(sampler2DArrayShadow, vec4)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec4"),
            ],
        ),
        "texture(sampler2DRect, vec2)": Func(
            return_type="vec4",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(isampler2DRect, vec2)": Func(
            return_type="ivec4",
            name="texture",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(usampler2DRect, vec2)": Func(
            return_type="uvec4",
            name="texture",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec2"),
            ],
        ),
        "texture(sampler2DRectShadow, vec3)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "texture(samplerCubeArrayShadow, vec4, float)": Func(
            return_type="float",
            name="texture",
            args=[
                Var(name="sampler", type="samplerCubeArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="compare", type="float"),
            ],
        ),
        "textureGather(sampler2D, vec2, int)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(sampler2D, vec2)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureGather(isampler2D, vec2, int)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(isampler2D, vec2)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureGather(usampler2D, vec2, int)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(usampler2D, vec2)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureGather(sampler2DArray, vec3, int)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(sampler2DArray, vec3)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(isampler2DArray, vec3, int)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(isampler2DArray, vec3)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(usampler2DArray, vec3, int)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(usampler2DArray, vec3)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(samplerCube, vec3, int)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(samplerCube, vec3)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(isamplerCube, vec3, int)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(isamplerCube, vec3)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(usamplerCube, vec3, int)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(usamplerCube, vec3)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(samplerCubeArray, vec4, int)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(samplerCubeArray, vec4)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureGather(isamplerCubeArray, vec4, int)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(isamplerCubeArray, vec4)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureGather(usamplerCubeArray, vec4, int)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(usamplerCubeArray, vec4)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureGather(sampler2DRect, vec3, int)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(sampler2DRect, vec3)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(isampler2DRect, vec3, int)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(isampler2DRect, vec3)": Func(
            return_type="ivec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(usampler2DRect, vec3, int)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGather(usampler2DRect, vec3)": Func(
            return_type="uvec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureGather(sampler2DShadow, vec2, float)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
            ],
        ),
        "textureGather(sampler2DArrayShadow, vec3, float)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="refZ", type="float"),
            ],
        ),
        "textureGather(samplerCubeShadow, vec3, float)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="P", type="vec3"),
                Var(name="refZ", type="float"),
            ],
        ),
        "textureGather(samplerCubeArrayShadow, vec4, float)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="samplerCubeArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="refZ", type="float"),
            ],
        ),
        "textureGather(sampler2DRectShadow, vec2, float)": Func(
            return_type="vec4",
            name="textureGather",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
            ],
        ),
        "textureGatherOffset(sampler2D, vec2, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(sampler2D, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(isampler2D, vec2, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(isampler2D, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(usampler2D, vec2, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(usampler2D, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(sampler2DArray, vec3, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(sampler2DArray, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(isampler2DArray, vec3, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(isampler2DArray, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(usampler2DArray, vec3, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(usampler2DArray, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(sampler2DRect, vec3, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(sampler2DRect, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(isampler2DRect, vec3, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(isampler2DRect, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(usampler2DRect, vec3, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffset(usampler2DRect, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(sampler2DShadow, vec2, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(sampler2DArrayShadow, vec3, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="refZ", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffset(sampler2DRectShadow, vec2, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffset",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGatherOffsets(sampler2D, vec2, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(sampler2D, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(isampler2D, vec2, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(isampler2D, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(usampler2D, vec2, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(usampler2D, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(sampler2DArray, vec3, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(sampler2DArray, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(isampler2DArray, vec3, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(isampler2DArray, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(usampler2DArray, vec3, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(usampler2DArray, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(sampler2DRect, vec3, ivec2, int)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(sampler2DRect, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(isampler2DRect, vec3, ivec2, int)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(isampler2DRect, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(usampler2DRect, vec3, ivec2, int)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
                Var(name="comp", type="int"),
            ],
        ),
        "textureGatherOffsets(usampler2DRect, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(sampler2DShadow, vec2, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(sampler2DArrayShadow, vec3, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="refZ", type="float"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGatherOffsets(sampler2DRectShadow, vec2, float, ivec2)": Func(
            return_type="vec4",
            name="textureGatherOffsets",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec2"),
                Var(name="refZ", type="float"),
                Var(name="offsets", type="ivec2[4]"),
            ],
        ),
        "textureGrad(sampler1D, float, float, float)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(isampler1D, float, float, float)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(usampler1D, float, float, float)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(sampler2D, vec2, vec2, vec2)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(isampler2D, vec2, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(usampler2D, vec2, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(sampler3D, vec3, vec3, vec3)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(isampler3D, vec3, vec3, vec3)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(usampler3D, vec3, vec3, vec3)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(samplerCube, vec3, vec3, vec3)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(isamplerCube, vec3, vec3, vec3)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(usamplerCube, vec3, vec3, vec3)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(sampler2DRect, vec2, vec2, vec2)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(isampler2DRect, vec2, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(usampler2DRect, vec2, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(sampler2DRectShadow, vec3, vec2, vec2)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(sampler1DShadow, vec3, float, float)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(sampler1DArray, vec2, float, float)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(isampler1DArray, vec2, float, float)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(usampler1DArray, vec2, float, float)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(sampler2DArray, vec3, vec2, vec2)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(isampler2DArray, vec3, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(usampler2DArray, vec3, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(sampler1DArrayShadow, vec3, float, float)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
            ],
        ),
        "textureGrad(sampler2DShadow, vec3, vec2, vec2)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(samplerCubeShadow, vec4, vec3, vec3)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(sampler2DArrayShadow, vec4, vec2, vec2)": Func(
            return_type="float",
            name="textureGrad",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
            ],
        ),
        "textureGrad(samplerCubeArray, vec4, vec3, vec3)": Func(
            return_type="vec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(isamplerCubeArray, vec4, vec3, vec3)": Func(
            return_type="ivec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGrad(usamplerCubeArray, vec4, vec3, vec3)": Func(
            return_type="uvec4",
            name="textureGrad",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
            ],
        ),
        "textureGradOffset(sampler1D, float, float, float, int)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(isampler1D, float, float, float, int)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(usampler1D, float, float, float, int)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(sampler2D, vec2, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(isampler2D, vec2, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(usampler2D, vec2, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(sampler3D, vec3, vec3, vec3, ivec3)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureGradOffset(isampler3D, vec3, vec3, vec3, ivec3)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureGradOffset(usampler3D, vec3, vec3, vec3, ivec3)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureGradOffset(sampler2DRect, vec2, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(isampler2DRect, vec2, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(usampler2DRect, vec2, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(sampler2DRectShadow, vec3, vec2, vec2, ivec2)": Func(
            return_type="float",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(sampler1DShadow, vec3, float, float, int)": Func(
            return_type="float",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(sampler2DShadow, vec3, vec2, vec2, ivec2)": Func(
            return_type="float",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(sampler1DArray, vec2, float, float, int)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(isampler1DArray, vec2, float, float, int)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(usampler1DArray, vec2, float, float, int)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(sampler2DArray, vec3, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(isampler2DArray, vec3, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(usampler2DArray, vec3, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureGradOffset(sampler1DArrayShadow, vec3, float, float, int)": Func(
            return_type="float",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureGradOffset(sampler2DArrayShadow, vec4, vec2, vec2, ivec2)": Func(
            return_type="float",
            name="textureGradOffset",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLod(sampler1D, float, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isampler1D, float, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usampler1D, float, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler2D, vec2, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isampler2D, vec2, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usampler2D, vec2, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler3D, vec3, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isampler3D, vec3, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usampler3D, vec3, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(samplerCube, vec3, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isamplerCube, vec3, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usamplerCube, vec3, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler1DShadow, vec3, float)": Func(
            return_type="float",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler2DShadow, vec3, float)": Func(
            return_type="float",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler1DArray, vec2, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isampler1DArray, vec2, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usampler1DArray, vec2, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler2DArray, vec3, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isampler2DArray, vec3, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usampler2DArray, vec3, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(sampler1DArrayShadow, vec3, float)": Func(
            return_type="float",
            name="textureLod",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(samplerCubeArray, vec4, float)": Func(
            return_type="vec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(isamplerCubeArray, vec4, float)": Func(
            return_type="ivec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLod(usamplerCubeArray, vec4, float)": Func(
            return_type="uvec4",
            name="textureLod",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureLodOffset(sampler1D, float, float, int)": Func(
            return_type="vec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(isampler1D, float, float, int)": Func(
            return_type="ivec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(usampler1D, float, float, int)": Func(
            return_type="uvec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(sampler2D, vec2, float, ivec2)": Func(
            return_type="vec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(isampler2D, vec2, float, ivec2)": Func(
            return_type="ivec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(usampler2D, vec2, float, ivec2)": Func(
            return_type="uvec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(sampler3D, vec3, float, ivec3)": Func(
            return_type="vec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureLodOffset(isampler3D, vec3, float, ivec3)": Func(
            return_type="ivec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureLodOffset(usampler3D, vec3, float, ivec3)": Func(
            return_type="uvec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureLodOffset(sampler1DShadow, vec3, float, int)": Func(
            return_type="float",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(sampler2DShadow, vec3, float, ivec2)": Func(
            return_type="float",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(sampler1DArray, vec2, float, int)": Func(
            return_type="vec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(isampler1DArray, vec2, float, int)": Func(
            return_type="ivec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(usampler1DArray, vec2, float, int)": Func(
            return_type="uvec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureLodOffset(sampler2DArray, vec3, float, ivec2)": Func(
            return_type="vec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(isampler2DArray, vec3, float, ivec2)": Func(
            return_type="ivec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(usampler2DArray, vec3, float, ivec2)": Func(
            return_type="uvec4",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureLodOffset(sampler1DArrayShadow, vec3, float, int)": Func(
            return_type="float",
            name="textureLodOffset",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(sampler1D, float, int, float)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler1D, float, int)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(isampler1D, float, int, float)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(isampler1D, float, int)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(usampler1D, float, int, float)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(usampler1D, float, int)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(sampler2D, vec2, ivec2, float)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler2D, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(isampler2D, vec2, ivec2, float)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(isampler2D, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(usampler2D, vec2, ivec2, float)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(usampler2D, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(sampler3D, vec3, ivec3, float)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler3D, vec3, ivec3)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureOffset(isampler3D, vec3, ivec3, float)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(isampler3D, vec3, ivec3)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureOffset(usampler3D, vec3, ivec3, float)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(usampler3D, vec3, ivec3)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureOffset(sampler2DRect, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(isampler2DRect, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(usampler2DRect, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(sampler2DRectShadow, vec3, ivec2)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(sampler1DShadow, vec3, int, float)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler1DShadow, vec3, int)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(sampler2DShadow, vec4, ivec2, float)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler2DShadow, vec4, ivec2)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(sampler1DArray, vec2, int, float)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler1DArray, vec2, int)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(isampler1DArray, vec2, int, float)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(isampler1DArray, vec2, int)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(usampler1DArray, vec2, int, float)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(usampler1DArray, vec2, int)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(sampler2DArray, vec3, ivec2, float)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(sampler2DArray, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(isampler2DArray, vec3, ivec2, float)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(isampler2DArray, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(usampler2DArray, vec3, ivec2, float)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureOffset(usampler2DArray, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureOffset",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureOffset(sampler1DArrayShadow, vec3, int)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureOffset(sampler2DArrayShadow, vec4, vec2)": Func(
            return_type="float",
            name="textureOffset",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="vec2"),
            ],
        ),
        "textureProj(sampler1D, vec2, float)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler1D, vec2)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureProj(isampler1D, vec2, float)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(isampler1D, vec2)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureProj(usampler1D, vec2, float)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(usampler1D, vec2)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureProj(sampler1D, vec4, float)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler1D, vec4)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(isampler1D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(isampler1D, vec4)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(usampler1D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(usampler1D, vec4)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler2D, vec3, float)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler2D, vec3)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(isampler2D, vec3, float)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(isampler2D, vec3)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(usampler2D, vec3, float)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(usampler2D, vec3)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(sampler2D, vec4, float)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler2D, vec4)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(isampler2D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(isampler2D, vec4)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(usampler2D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(usampler2D, vec4)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler3D, vec4, float)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler3D, vec4)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(isampler3D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(isampler3D, vec4)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(usampler3D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(usampler3D, vec4)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler1DShadow, vec4, float)": Func(
            return_type="float",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler1DShadow, vec4)": Func(
            return_type="float",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler2DShadow, vec4, float)": Func(
            return_type="float",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProj(sampler2DShadow, vec4)": Func(
            return_type="float",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler2DRect, vec3)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(isampler2DRect, vec3)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(usampler2DRect, vec3)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureProj(sampler2DRect, vec4)": Func(
            return_type="vec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(isampler2DRect, vec4)": Func(
            return_type="ivec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(usampler2DRect, vec4)": Func(
            return_type="uvec4",
            name="textureProj",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProj(sampler2DRectShadow, vec4)": Func(
            return_type="float",
            name="textureProj",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec4"),
            ],
        ),
        "textureProjGrad(sampler1D, vec2, float, float)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(isampler1D, vec2, float, float)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(usampler1D, vec2, float, float)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(sampler1D, vec4, float, float)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(isampler1D, vec4, float, float)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(usampler1D, vec4, float, float)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(sampler2D, vec3, vec2, vec2)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(isampler2D, vec3, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(usampler2D, vec3, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(sampler2D, vec4, vec2, vec2)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(isampler2D, vec4, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(usampler2D, vec4, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(sampler3D, vec4, vec3, vec3)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec3"),
                Var(name="pDy", type="vec3"),
            ],
        ),
        "textureProjGrad(isampler3D, vec4, vec3, vec3)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec3"),
                Var(name="pDy", type="vec3"),
            ],
        ),
        "textureProjGrad(usampler3D, vec4, vec3, vec3)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec3"),
                Var(name="pDy", type="vec3"),
            ],
        ),
        "textureProjGrad(sampler1DShadow, vec4, float, float)": Func(
            return_type="float",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="float"),
                Var(name="pDy", type="float"),
            ],
        ),
        "textureProjGrad(sampler2DShadow, vec4, vec2, vec2)": Func(
            return_type="float",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(sampler2DRect, vec3, vec2, vec2)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(isampler2DRect, vec3, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(usampler2DRect, vec3, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(sampler2DRect, vec4, vec2, vec2)": Func(
            return_type="vec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(isampler2DRect, vec4, vec2, vec2)": Func(
            return_type="ivec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(usampler2DRect, vec4, vec2, vec2)": Func(
            return_type="uvec4",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGrad(sampler2DRectShadow, vec4, vec2, vec2)": Func(
            return_type="float",
            name="textureProjGrad",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec4"),
                Var(name="pDx", type="vec2"),
                Var(name="pDy", type="vec2"),
            ],
        ),
        "textureProjGradOffset(sampler1D, vec2, float, float, int)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(isampler1D, vec2, float, float, int)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(usampler1D, vec2, float, float, int)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(sampler1D, vec4, float, float, int)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(isampler1D, vec4, float, float, int)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(usampler1D, vec4, float, float, int)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(sampler2D, vec3, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(isampler2D, vec3, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(usampler2D, vec3, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(sampler2D, vec4, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(isampler2D, vec4, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(usampler2D, vec4, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(sampler3D, vec4, vec3, vec3, ivec3)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjGradOffset(isampler3D, vec4, vec3, vec3, ivec3)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjGradOffset(usampler3D, vec4, vec3, vec3, ivec3)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec3"),
                Var(name="dPdy", type="vec3"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjGradOffset(sampler1DShadow, vec4, float, float, int)": Func(
            return_type="float",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="float"),
                Var(name="dPdy", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjGradOffset(sampler2DShadow, vec4, vec2, vec2, ivec2)": Func(
            return_type="float",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(sampler2DRect, vec3, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(isampler2DRect, vec3, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(usampler2DRect, vec3, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(sampler2DRect, vec4, vec2, vec2, ivec2)": Func(
            return_type="vec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(isampler2DRect, vec4, vec2, vec2, ivec2)": Func(
            return_type="ivec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(usampler2DRect, vec4, vec2, vec2, ivec2)": Func(
            return_type="uvec4",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjGradOffset(sampler2DRectShadow, vec4, vec2, vec2, ivec2)": Func(
            return_type="float",
            name="textureProjGradOffset",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec4"),
                Var(name="dPdx", type="vec2"),
                Var(name="dPdy", type="vec2"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLod(sampler1D, vec2, float)": Func(
            return_type="vec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(isampler1D, vec2, float)": Func(
            return_type="ivec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(usampler1D, vec2, float)": Func(
            return_type="uvec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler1D, vec4, float)": Func(
            return_type="vec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(isampler1D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(usampler1D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler2D, vec3, float)": Func(
            return_type="vec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(isampler2D, vec3, float)": Func(
            return_type="ivec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(usampler2D, vec3, float)": Func(
            return_type="uvec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler2D, vec4, float)": Func(
            return_type="vec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(isampler2D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(usampler2D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler3D, vec4, float)": Func(
            return_type="vec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(isampler3D, vec4, float)": Func(
            return_type="ivec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(usampler3D, vec4, float)": Func(
            return_type="uvec4",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler1DShadow, vec4, float)": Func(
            return_type="float",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLod(sampler2DShadow, vec4, float)": Func(
            return_type="float",
            name="textureProjLod",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
            ],
        ),
        "textureProjLodOffset(sampler1D, vec2, float, int)": Func(
            return_type="vec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(isampler1D, vec2, float, int)": Func(
            return_type="ivec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(usampler1D, vec2, float, int)": Func(
            return_type="uvec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(sampler1D, vec4, float, int)": Func(
            return_type="vec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(isampler1D, vec4, float, int)": Func(
            return_type="ivec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(usampler1D, vec4, float, int)": Func(
            return_type="uvec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(sampler2D, vec3, float, ivec2)": Func(
            return_type="vec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(isampler2D, vec3, float, ivec2)": Func(
            return_type="ivec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(usampler2D, vec3, float, ivec2)": Func(
            return_type="uvec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(sampler2D, vec4, float, ivec2)": Func(
            return_type="vec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(isampler2D, vec4, float, ivec2)": Func(
            return_type="ivec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(usampler2D, vec4, float, ivec2)": Func(
            return_type="uvec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjLodOffset(sampler3D, vec4, float, ivec3)": Func(
            return_type="vec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjLodOffset(isampler3D, vec4, float, ivec3)": Func(
            return_type="ivec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjLodOffset(usampler3D, vec4, float, ivec3)": Func(
            return_type="uvec4",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjLodOffset(sampler1DShadow, vec4, float, int)": Func(
            return_type="float",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjLodOffset(sampler2DShadow, vec4, float, ivec2)": Func(
            return_type="float",
            name="textureProjLodOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="lod", type="float"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler1D, vec2, int, float)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler1D, vec2, int)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(isampler1D, vec2, int, float)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(isampler1D, vec2, int)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(usampler1D, vec2, int, float)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(usampler1D, vec2, int)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec2"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(sampler1D, vec4, int, float)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler1D, vec4, int)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(isampler1D, vec4, int, float)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(isampler1D, vec4, int)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(usampler1D, vec4, int, float)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(usampler1D, vec4, int)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(sampler2D, vec3, ivec2, float)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler2D, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(isampler2D, vec3, ivec2, float)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(isampler2D, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(usampler2D, vec3, ivec2, float)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(usampler2D, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler2D, vec4, ivec2, float)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler2D, vec4, ivec2)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(isampler2D, vec4, ivec2, float)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(isampler2D, vec4, ivec2)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(usampler2D, vec4, ivec2, float)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(usampler2D, vec4, ivec2)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler3D, vec4, ivec3, float)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler3D, vec4, ivec3)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjOffset(isampler3D, vec4, ivec3, float)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(isampler3D, vec4, ivec3)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjOffset(usampler3D, vec4, ivec3, float)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(usampler3D, vec4, ivec3)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec3"),
            ],
        ),
        "textureProjOffset(sampler1DShadow, vec4, int, float)": Func(
            return_type="float",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler1DShadow, vec4, int)": Func(
            return_type="float",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="int"),
            ],
        ),
        "textureProjOffset(sampler2DShadow, vec4, ivec2, float)": Func(
            return_type="float",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
                Var(name="bias", type="float"),
            ],
        ),
        "textureProjOffset(sampler2DShadow, vec4, ivec2)": Func(
            return_type="float",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler2DRect, vec3, ivec2)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(isampler2DRect, vec3, ivec2)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(usampler2DRect, vec3, ivec2)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec3"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler2DRect, vec4, ivec2)": Func(
            return_type="vec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(isampler2DRect, vec4, ivec2)": Func(
            return_type="ivec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="isampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(usampler2DRect, vec4, ivec2)": Func(
            return_type="uvec4",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="usampler2DRect"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureProjOffset(sampler2DRectShadow, vec4, ivec2)": Func(
            return_type="float",
            name="textureProjOffset",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
                Var(name="P", type="vec4"),
                Var(name="offset", type="ivec2"),
            ],
        ),
        "textureQueryLevels(sampler1D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler1D"),
            ],
        ),
        "textureQueryLevels(isampler1D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isampler1D"),
            ],
        ),
        "textureQueryLevels(usampler1D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usampler1D"),
            ],
        ),
        "textureQueryLevels(sampler2D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler2D"),
            ],
        ),
        "textureQueryLevels(isampler2D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isampler2D"),
            ],
        ),
        "textureQueryLevels(usampler2D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usampler2D"),
            ],
        ),
        "textureQueryLevels(sampler3D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler3D"),
            ],
        ),
        "textureQueryLevels(isampler3D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isampler3D"),
            ],
        ),
        "textureQueryLevels(usampler3D)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usampler3D"),
            ],
        ),
        "textureQueryLevels(samplerCube)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="samplerCube"),
            ],
        ),
        "textureQueryLevels(isamplerCube)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isamplerCube"),
            ],
        ),
        "textureQueryLevels(usamplerCube)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usamplerCube"),
            ],
        ),
        "textureQueryLevels(sampler1DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler1DArray"),
            ],
        ),
        "textureQueryLevels(isampler1DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isampler1DArray"),
            ],
        ),
        "textureQueryLevels(usampler1DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usampler1DArray"),
            ],
        ),
        "textureQueryLevels(sampler2DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler2DArray"),
            ],
        ),
        "textureQueryLevels(isampler2DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isampler2DArray"),
            ],
        ),
        "textureQueryLevels(usampler2DArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usampler2DArray"),
            ],
        ),
        "textureQueryLevels(samplerCubeArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
            ],
        ),
        "textureQueryLevels(isamplerCubeArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
            ],
        ),
        "textureQueryLevels(usamplerCubeArray)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
            ],
        ),
        "textureQueryLevels(sampler1DShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
            ],
        ),
        "textureQueryLevels(sampler2DShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
            ],
        ),
        "textureQueryLevels(samplerCubeShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
            ],
        ),
        "textureQueryLevels(sampler1DArrayShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
            ],
        ),
        "textureQueryLevels(sampler2DArrayShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
            ],
        ),
        "textureQueryLevels(samplerCubeArrayShadow)": Func(
            return_type="int",
            name="textureQueryLevels",
            args=[
                Var(name="sampler", type="samplerCubeArrayShadow"),
            ],
        ),
        "textureQueryLod(sampler1D, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(isampler1D, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(usampler1D, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(sampler2D, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(isampler2D, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(usampler2D, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(sampler3D, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(isampler3D, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(usampler3D, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(samplerCube, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(isamplerCube, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(usamplerCube, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(sampler1DArray, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(isampler1DArray, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(usampler1DArray, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(sampler2DArray, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(isampler2DArray, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(usampler2DArray, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(samplerCubeArray, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(isamplerCubeArray, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="isamplerCubeArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(usamplerCubeArray, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="usamplerCubeArray"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(sampler1DShadow, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(sampler2DShadow, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(samplerCubeShadow, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureQueryLod(sampler1DArrayShadow, float)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="P", type="float"),
            ],
        ),
        "textureQueryLod(sampler2DArrayShadow, vec2)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="P", type="vec2"),
            ],
        ),
        "textureQueryLod(samplerCubeArrayShadow, vec3)": Func(
            return_type="vec2",
            name="textureQueryLod",
            args=[
                Var(name="sampler", type="samplerCubeArrayShadow"),
                Var(name="P", type="vec3"),
            ],
        ),
        "textureSamples(sampler2DMS)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="sampler2DMS"),
            ],
        ),
        "textureSamples(isampler2DMS)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="isampler2DMS"),
            ],
        ),
        "textureSamples(usampler2DMS)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="usampler2DMS"),
            ],
        ),
        "textureSamples(sampler2DMSArray)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="sampler2DMSArray"),
            ],
        ),
        "textureSamples(isampler2DMSArray)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="isampler2DMSArray"),
            ],
        ),
        "textureSamples(usampler2DMSArray)": Func(
            return_type="int",
            name="textureSamples",
            args=[
                Var(name="sampler", type="usampler2DMSArray"),
            ],
        ),
        "textureSize(sampler1D, int)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler1D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isampler1D, int)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler1D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usampler1D, int)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler1D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler2D, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isampler2D, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler2D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usampler2D, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler2D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler3D, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler3D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isampler3D, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler3D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usampler3D, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler3D"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(samplerCube, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="samplerCube"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isamplerCube, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="isamplerCube"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usamplerCube, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="usamplerCube"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler1DShadow, int)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler1DShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler2DShadow, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(samplerCubeShadow, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="samplerCubeShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(samplerCubeArray, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="samplerCubeArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(samplerCubeArrayShadow, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="samplerCubeArrayShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler2DRect)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DRect"),
            ],
        ),
        "textureSize(isampler2DRect)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler2DRect"),
            ],
        ),
        "textureSize(usampler2DRect)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler2DRect"),
            ],
        ),
        "textureSize(sampler2DRectShadow)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DRectShadow"),
            ],
        ),
        "textureSize(sampler1DArray, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler1DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isampler1DArray, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler1DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usampler1DArray, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler1DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler2DArray, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(isampler2DArray, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler2DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(usampler2DArray, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler2DArray"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler1DArrayShadow, int)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler1DArrayShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(sampler2DArrayShadow, int)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DArrayShadow"),
                Var(name="lod", type="int"),
            ],
        ),
        "textureSize(samplerBuffer)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="samplerBuffer"),
            ],
        ),
        "textureSize(isamplerBuffer)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="isamplerBuffer"),
            ],
        ),
        "textureSize(usamplerBuffer)": Func(
            return_type="int",
            name="textureSize",
            args=[
                Var(name="sampler", type="usamplerBuffer"),
            ],
        ),
        "textureSize(sampler2DMS)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DMS"),
            ],
        ),
        "textureSize(isampler2DMS)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler2DMS"),
            ],
        ),
        "textureSize(usampler2DMS)": Func(
            return_type="ivec2",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler2DMS"),
            ],
        ),
        "textureSize(sampler2DMSArray)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="sampler2DMSArray"),
            ],
        ),
        "textureSize(isampler2DMSArray)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="isampler2DMSArray"),
            ],
        ),
        "textureSize(usampler2DMSArray)": Func(
            return_type="ivec3",
            name="textureSize",
            args=[
                Var(name="sampler", type="usampler2DMSArray"),
            ],
        ),
        "transpose(mat2)": Func(
            return_type="mat2",
            name="transpose",
            args=[
                Var(name="m", type="mat2"),
            ],
        ),
        "transpose(mat3)": Func(
            return_type="mat3",
            name="transpose",
            args=[
                Var(name="m", type="mat3"),
            ],
        ),
        "transpose(mat4)": Func(
            return_type="mat4",
            name="transpose",
            args=[
                Var(name="m", type="mat4"),
            ],
        ),
        "transpose(mat3x2)": Func(
            return_type="mat2x3",
            name="transpose",
            args=[
                Var(name="m", type="mat3x2"),
            ],
        ),
        "transpose(mat4x2)": Func(
            return_type="mat2x4",
            name="transpose",
            args=[
                Var(name="m", type="mat4x2"),
            ],
        ),
        "transpose(mat2x3)": Func(
            return_type="mat3x2",
            name="transpose",
            args=[
                Var(name="m", type="mat2x3"),
            ],
        ),
        "transpose(mat4x3)": Func(
            return_type="mat3x4",
            name="transpose",
            args=[
                Var(name="m", type="mat4x3"),
            ],
        ),
        "transpose(mat2x4)": Func(
            return_type="mat4x2",
            name="transpose",
            args=[
                Var(name="m", type="mat2x4"),
            ],
        ),
        "transpose(mat3x4)": Func(
            return_type="mat4x3",
            name="transpose",
            args=[
                Var(name="m", type="mat3x4"),
            ],
        ),
        "transpose(dmat2)": Func(
            return_type="dmat2",
            name="transpose",
            args=[
                Var(name="m", type="dmat2"),
            ],
        ),
        "transpose(dmat3)": Func(
            return_type="dmat3",
            name="transpose",
            args=[
                Var(name="m", type="dmat3"),
            ],
        ),
        "transpose(dmat4)": Func(
            return_type="dmat4",
            name="transpose",
            args=[
                Var(name="m", type="dmat4"),
            ],
        ),
        "transpose(dmat3x2)": Func(
            return_type="dmat2x3",
            name="transpose",
            args=[
                Var(name="m", type="dmat3x2"),
            ],
        ),
        "transpose(dmat4x2)": Func(
            return_type="dmat2x4",
            name="transpose",
            args=[
                Var(name="m", type="dmat4x2"),
            ],
        ),
        "transpose(dmat2x3)": Func(
            return_type="dmat3x2",
            name="transpose",
            args=[
                Var(name="m", type="dmat2x3"),
            ],
        ),
        "transpose(dmat4x3)": Func(
            return_type="dmat3x4",
            name="transpose",
            args=[
                Var(name="m", type="dmat4x3"),
            ],
        ),
        "transpose(dmat2x4)": Func(
            return_type="dmat4x2",
            name="transpose",
            args=[
                Var(name="m", type="dmat2x4"),
            ],
        ),
        "transpose(dmat3x4)": Func(
            return_type="dmat4x3",
            name="transpose",
            args=[
                Var(name="m", type="dmat3x4"),
            ],
        ),
        "trunc(float)": Func(
            return_type="float",
            name="trunc",
            args=[
                Var(name="x", type="float"),
            ],
        ),
        "trunc(vec2)": Func(
            return_type="vec2",
            name="trunc",
            args=[
                Var(name="x", type="vec2"),
            ],
        ),
        "trunc(vec3)": Func(
            return_type="vec3",
            name="trunc",
            args=[
                Var(name="x", type="vec3"),
            ],
        ),
        "trunc(vec4)": Func(
            return_type="vec4",
            name="trunc",
            args=[
                Var(name="x", type="vec4"),
            ],
        ),
        "trunc(double)": Func(
            return_type="double",
            name="trunc",
            args=[
                Var(name="x", type="double"),
            ],
        ),
        "trunc(dvec2)": Func(
            return_type="dvec2",
            name="trunc",
            args=[
                Var(name="x", type="dvec2"),
            ],
        ),
        "trunc(dvec3)": Func(
            return_type="dvec3",
            name="trunc",
            args=[
                Var(name="x", type="dvec3"),
            ],
        ),
        "trunc(dvec4)": Func(
            return_type="dvec4",
            name="trunc",
            args=[
                Var(name="x", type="dvec4"),
            ],
        ),
        "uaddCarry(uint, uint, uint)": Func(
            return_type="uint",
            name="uaddCarry",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
                Var(name="carry", type="uint"),
            ],
        ),
        "uaddCarry(uvec2, uvec2, uvec2)": Func(
            return_type="uvec2",
            name="uaddCarry",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
                Var(name="carry", type="uvec2"),
            ],
        ),
        "uaddCarry(uvec3, uvec3, uvec3)": Func(
            return_type="uvec3",
            name="uaddCarry",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
                Var(name="carry", type="uvec3"),
            ],
        ),
        "uaddCarry(uvec4, uvec4, uvec4)": Func(
            return_type="uvec4",
            name="uaddCarry",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
                Var(name="carry", type="uvec4"),
            ],
        ),
        "umulExtended(uint, uint, uint, uint)": Func(
            return_type="void",
            name="umulExtended",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
                Var(name="msb", type="uint"),
                Var(name="lsb", type="uint"),
            ],
        ),
        "umulExtended(uvec2, uvec2, uvec2, uvec2)": Func(
            return_type="void",
            name="umulExtended",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
                Var(name="msb", type="uvec2"),
                Var(name="lsb", type="uvec2"),
            ],
        ),
        "umulExtended(uvec3, uvec3, uvec3, uvec3)": Func(
            return_type="void",
            name="umulExtended",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
                Var(name="msb", type="uvec3"),
                Var(name="lsb", type="uvec3"),
            ],
        ),
        "umulExtended(uvec4, uvec4, uvec4, uvec4)": Func(
            return_type="void",
            name="umulExtended",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
                Var(name="msb", type="uvec4"),
                Var(name="lsb", type="uvec4"),
            ],
        ),
        "imulExtended(int, int, int, int)": Func(
            return_type="void",
            name="imulExtended",
            args=[
                Var(name="x", type="int"),
                Var(name="y", type="int"),
                Var(name="msb", type="int"),
                Var(name="lsb", type="int"),
            ],
        ),
        "imulExtended(ivec2, ivec2, ivec2, ivec2)": Func(
            return_type="void",
            name="imulExtended",
            args=[
                Var(name="x", type="ivec2"),
                Var(name="y", type="ivec2"),
                Var(name="msb", type="ivec2"),
                Var(name="lsb", type="ivec2"),
            ],
        ),
        "imulExtended(ivec3, ivec3, ivec3, ivec3)": Func(
            return_type="void",
            name="imulExtended",
            args=[
                Var(name="x", type="ivec3"),
                Var(name="y", type="ivec3"),
                Var(name="msb", type="ivec3"),
                Var(name="lsb", type="ivec3"),
            ],
        ),
        "imulExtended(ivec4, ivec4, ivec4, ivec4)": Func(
            return_type="void",
            name="imulExtended",
            args=[
                Var(name="x", type="ivec4"),
                Var(name="y", type="ivec4"),
                Var(name="msb", type="ivec4"),
                Var(name="lsb", type="ivec4"),
            ],
        ),
        "unpackDouble2x32(double)": Func(
            return_type="uvec2",
            name="unpackDouble2x32",
            args=[
                Var(name="d", type="double"),
            ],
        ),
        "unpackHalf2x16(uint)": Func(
            return_type="vec2",
            name="unpackHalf2x16",
            args=[
                Var(name="v", type="uint"),
            ],
        ),
        "unpackUnorm2x16(uint)": Func(
            return_type="vec2",
            name="unpackUnorm2x16",
            args=[
                Var(name="p", type="uint"),
            ],
        ),
        "unpackSnorm2x16(uint)": Func(
            return_type="vec2",
            name="unpackSnorm2x16",
            args=[
                Var(name="p", type="uint"),
            ],
        ),
        "unpackUnorm4x8(uint)": Func(
            return_type="vec4",
            name="unpackUnorm4x8",
            args=[
                Var(name="p", type="uint"),
            ],
        ),
        "unpackSnorm4x8(uint)": Func(
            return_type="vec4",
            name="unpackSnorm4x8",
            args=[
                Var(name="p", type="uint"),
            ],
        ),
        "usubBorrow(uint, uint, uint)": Func(
            return_type="uint",
            name="usubBorrow",
            args=[
                Var(name="x", type="uint"),
                Var(name="y", type="uint"),
                Var(name="borrow", type="uint"),
            ],
        ),
        "usubBorrow(uvec2, uvec2, uvec2)": Func(
            return_type="uvec2",
            name="usubBorrow",
            args=[
                Var(name="x", type="uvec2"),
                Var(name="y", type="uvec2"),
                Var(name="borrow", type="uvec2"),
            ],
        ),
        "usubBorrow(uvec3, uvec3, uvec3)": Func(
            return_type="uvec3",
            name="usubBorrow",
            args=[
                Var(name="x", type="uvec3"),
                Var(name="y", type="uvec3"),
                Var(name="borrow", type="uvec3"),
            ],
        ),
        "usubBorrow(uvec4, uvec4, uvec4)": Func(
            return_type="uvec4",
            name="usubBorrow",
            args=[
                Var(name="x", type="uvec4"),
                Var(name="y", type="uvec4"),
                Var(name="borrow", type="uvec4"),
            ],
        ),
    }

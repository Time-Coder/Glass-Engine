// Day and night sky cycle. By László Matuska (@BitOfGold)
// Creates a sky texture for a skydome
// https://www.shadertoy.com/view/ltlSWB


// based on other shaders, Greetings goes to:

// Weather. By David Hoskins, May 2014.
// https://www.shadertoy.com/view/4dsXWn

// Edge of atmosphere
// created by dmytro rubalskyi (ruba)
// https://www.shadertoy.com/view/XlXGzB

// Starfield01 by xaot88
// https://www.shadertoy.com/view/Md2SR3
// ======================================================================

#define shadertoy 1
#define clouds 1
#define stars 1
//#define cloud2 1 //second layer of clouds, altocumulus or stratocumulus. (in 4K, too slow on my GTX970. HD is OK.)
//plan was to make cirrus too...

//rendering quality 
const int steps = 132; //16 is fast, 128 or 256 is extreme high
const int stepss = 16; //16 is fast, 16 or 32 is high 

#ifdef GL_ES
precision highp float;
#endif

const float M_PI = 3.1415926535;
const float DEGRAD = M_PI / 180.0;

#ifdef shadertoy
	float height = 500.0; //viewer height
    float cloudy = 0.6; //0.6 //0.0 clear sky
#else
    varying vec3 vNormal;
    varying vec2 vUV;
    uniform sampler2D iChannel0;
    uniform float sunx;
    uniform float suny;
    uniform float moonx;
    uniform float moony;
    uniform float cloudy;
    uniform float height;
    uniform float time;
#endif

//float t = 12.0; //fix time. 12.0 91.0, 97.0, 188.0, 72.0, 74.0

float camroty = 0. * DEGRAD; //20.
float haze = 0.1; //0.2
float cloudyhigh = 0.05; //if cloud2 defined

float cloudnear = 1.0; //9e3 12e3  //do not render too close clouds on the zenith
float cloudfar = 1e3; //15e3 17e3

float startreshold = 0.99; //0.99 0.98 star density treshold.

const float I = 10.; //sun light power, 10.0 is normal
const float g = 0.45; //light concentration .76 //.45 //.6  .45 is normaL
const float g2 = g * g;

//Reyleigh scattering (sky color, atmospheric up to 8km)
vec3 bR = vec3(5.8e-6, 13.5e-6, 33.1e-6); //normal earth
//vec3 bR = vec3(5.8e-6, 33.1e-6, 13.5e-6); //purple
//vec3 bR = vec3( 63.5e-6, 13.1e-6, 50.8e-6 ); //green
//vec3 bR = vec3( 13.5e-6, 23.1e-6, 115.8e-6 ); //yellow
//vec3 bR = vec3( 5.5e-6, 15.1e-6, 355.8e-6 ); //yeellow
//vec3 bR = vec3(3.5e-6, 333.1e-6, 235.8e-6 ); //red-purple

//Mie scattering (water particles up to 1km)
vec3 bM = vec3(21e-6); //normal mie
//vec3 bM = vec3(50e-6); //high mie

//-----
//positions

const float Hr = 8000.0; //Reyleight scattering top
const float Hm = 1000.0; //Mie scattering top

const float R0 = 6360e3; //planet radius
const float Ra = 6380e3; //atmosphere radius
vec3 C = vec3(0., -R0, 0.); //planet center
vec3 Ds = normalize(vec3(0., .09, -1.)); //sun direction?

//--------------------------------------------------------------------------
//Starfield
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.

// Return random noise in the range [0.0, 1.0], as a function of x.
float Noise2d( in vec2 x )
{
    float xhash = cos( x.x * 37.0 );
    float yhash = cos( x.y * 57.0 );
    return fract( 415.92653 * ( xhash + yhash ) );
}

// Convert Noise2d() into a "star field" by stomping everthing below fThreshhold to zero.
float NoisyStarField( in vec2 vSamplePos, float fThreshhold )
{
    float StarVal = Noise2d( vSamplePos );
    if ( StarVal >= fThreshhold )
        StarVal = pow( (StarVal - fThreshhold)/(1.0 - fThreshhold), 6.0 );
    else
        StarVal = 0.0;
    return StarVal;
}

// Stabilize NoisyStarField() by only sampling at integer values.
float StableStarField( in vec2 vSamplePos, float fThreshhold )
{
    // Linear interpolation between four samples.
    // Note: This approach has some visual artifacts.
    // There must be a better way to "anti alias" the star field.
    float fractX = fract( vSamplePos.x );
    float fractY = fract( vSamplePos.y );
    vec2 floorSample = floor( vSamplePos );    
    float v1 = NoisyStarField( floorSample, fThreshhold );
    float v2 = NoisyStarField( floorSample + vec2( 0.0, 1.0 ), fThreshhold );
    float v3 = NoisyStarField( floorSample + vec2( 1.0, 0.0 ), fThreshhold );
    float v4 = NoisyStarField( floorSample + vec2( 1.0, 1.0 ), fThreshhold );

    float StarVal =   v1 * ( 1.0 - fractX ) * ( 1.0 - fractY )
        			+ v2 * ( 1.0 - fractX ) * fractY
        			+ v3 * fractX * ( 1.0 - fractY )
        			+ v4 * fractX * fractY;
	return StarVal;
}


//--------------------------------------------------------------------------
//Cloud noise

float Noise( in vec3 x )
{
    vec3 p = floor(x);
    vec3 f = fract(x);
	f = f*f*(3.0-2.0*f);

	vec2 uv = (p.xy+vec2(37.0,17.0)*p.z) + f.xy;
	vec2 rg = texture( iChannel0, (uv+ 0.5)/256.0, -100.0).yx;
	return mix( rg.x, rg.y, f.z );
}

float fnoise( vec3 p, in float t )
{
	p *= .25;
    float f;

	f = 0.5000 * Noise(p); p = p * 3.02; p.y -= t*.2;
	f += 0.2500 * Noise(p); p = p * 3.03; p.y += t*.06;
	f += 0.1250 * Noise(p); p = p * 3.01;
	f += 0.0625   * Noise(p); p =  p * 3.03;
	f += 0.03125  * Noise(p); p =  p * 3.02;
	f += 0.015625 * Noise(p);
    return f;
}

//--------------------------------------------------------------------------
//clouds, scattering

float cloud(vec3 p, in float t) {
	float cld = fnoise(p*2e-4,t) + cloudy*0.1 ;
	cld = smoothstep(.4+.04, .6+.04, cld);
	cld *= 70.;
	return cld+haze;
}


void densities(in vec3 pos, out float rayleigh, out float mie, in float t) {
	float h = length(pos - C) - R0;
	rayleigh =  exp(-h/Hr);
	vec3 d = pos;
    d.y = 0.0;
    float dist = length(d);
    #ifdef clouds
        float cld = 0.;
        if (5e3 < h && h < 8e3) {
            cld = cloud(pos+vec3(23175.7, 0.,-t*3e3), t);
            cld *= sin(3.1415*(h-5e3)/5e3) * cloudy;
        }
        #ifdef cloud2
            float cld2 = 0.;
            if (12e3 < h && h < 15.5e3) {
                cld2 = fnoise(pos*3e-4,t)*cloud(pos*32.0+vec3(27612.3, 0.,-t*15e3), t);
                cld2 *= sin(3.1413*(h-12e3)/12e3) * cloudyhigh;
                cld2 = clamp(cld2,0.0,1.0);
            }

        #endif

        if (dist<cloudfar) {
            float factor = clamp(1.0-((cloudfar - dist)/(cloudfar-cloudnear)),0.0,1.0);
            cld *= factor;
        }

        mie = exp(-h/Hm) + cld + haze;
        #ifdef cloud2
            mie += cld2;
        #endif
    #else
        mie = exp(-h/Hm) + haze;
    #endif
}

float escape(in vec3 p, in vec3 d, in float R) {
	vec3 v = p - C;
	float b = dot(v, d);
	float c = dot(v, v) - R*R;
	float det2 = b * b - c;
	if (det2 < 0.) return -1.;
	float det = sqrt(det2);
	float t1 = -b - det, t2 = -b + det;
	return (t1 >= 0.) ? t1 : t2;
}

// this can be explained: http://www.scratchapixel.com/lessons/3d-advanced-lessons/simulating-the-colors-of-the-sky/atmospheric-scattering/
void scatter(vec3 o, vec3 d, out vec3 col, out float scat, in float t) {
	float L = escape(o, d, Ra);
	float mu = dot(d, Ds);
	float opmu2 = 1. + mu*mu;
	float phaseR = .0596831 * opmu2;
	float phaseM = .1193662 * (1. - g2) * opmu2 / ((2. + g2) * pow(1. + g2 - 2.*g*mu, 1.5));

	float depthR = 0., depthM = 0.;
	vec3 R = vec3(0.), M = vec3(0.);

	float dl = L / float(steps);
	for (int i = 0; i < steps; ++i) {
		float l = float(i) * dl;
		vec3 p = o + d * l;

		float dR, dM;
		densities(p, dR, dM, t);
		dR *= dl; dM *= dl;
		depthR += dR;
		depthM += dM;

		float Ls = escape(p, Ds, Ra);
		if (Ls > 0.) {
			float dls = Ls / float(stepss);
			float depthRs = 0., depthMs = 0.;
			for (int j = 0; j < stepss; ++j) {
				float ls = float(j) * dls;
				vec3 ps = p + Ds * ls;
				float dRs, dMs;
				densities(ps, dRs, dMs, t);
				depthRs += dRs * dls;
				depthMs += dMs * dls;
			}

			vec3 A = exp(-(bR * (depthRs + depthR) + bM * (depthMs + depthM)));
			R += A * dR;
			M += A * dM;
		}
	}


	col = I * (R * bR * phaseR + M * bM * phaseM);
    scat = 1.0 - clamp(depthM*1e-5,0.,1.);    
}

//--------------------------------------------------------------------------
// ray casting

vec3 rotate_y(vec3 v, float angle)
{
	float ca = cos(angle); float sa = sin(angle);
	return v*mat3(
		+ca, +.0, -sa,
		+.0,+1.0, +.0,
		+sa, +.0, +ca);
}

vec3 rotate_x(vec3 v, float angle)
{
	float ca = cos(angle); float sa = sin(angle);
	return v*mat3(
		+1.0, +.0, +.0,
		+.0, +ca, -sa,
		+.0, +sa, +ca);
}

vec4 generate(in vec2 uv, in vec2 fragCoord, in vec2 sunpos, in float t) {
    
    //moon
    float att = 1.0;
    float staratt = 0.0;
    if (sunpos.y < -0.20) {
        sunpos.y = -sunpos.y;
        att = 0.25;
        staratt = 1.0;
    }
    
	vec3 O = vec3(0., height, 0.);

    vec3 D = normalize(rotate_y(rotate_x(vec3(0.0, 0.0, 1.0),-uv.y*M_PI/2.0),-uv.x*M_PI+camroty));

    if (D.y <= -0.15) {
        D.y = -0.3 -D.y;
    }
    
    Ds= normalize(rotate_y(rotate_x(vec3(0.0, 0.0, 1.0),-sunpos.y*M_PI/2.0),-sunpos.x*M_PI));
    float scat = 0.;
	vec3 color = vec3(0.);
    scatter(O, D, color, scat, t);
    color *= att;
    #ifdef stars
        float starcolor = StableStarField(fragCoord,startreshold);
        color += vec3(scat*starcolor*staratt);
    #endif
	float env = 0.9;
	return(vec4(env * pow(color, vec3(0.4)),1.0));
}

#ifdef shadertoy
    void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
        float t = iTime/2.0;
        float ymul = 2.0; float ydiff = -1.0;
        vec2 uv = fragCoord.xy / iResolution.xy;
        uv.x = 2.0 * uv.x - 1.0;
        uv.y = ymul * uv.y + ydiff;
        
        vec2 mouse = iMouse.xy / iResolution.xy;
        mouse.x = 2.0 * mouse.x + 1.0;
        mouse.y = 2.0 * mouse.y - 1.0;
        
        vec2 sunpos = mouse; // mouse sun/moon position
        
        fragColor = generate(uv,fragCoord,sunpos,t);
    }
#else
    void main() {
        vec2 uv = vec2(2.0 * vUV.x - 1.0,  -2.0 *  vUV.y + 1.0);
        vec2 sunpos = vec2(sunx,suny);
        float t = time;
        gl_FragColor = generate(uv,uv,sunpos,t);
    }
#endif

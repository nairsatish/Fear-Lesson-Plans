:pyr2pyr synapse with AMPA+NMDA and local Ca2+ pools that control plasticity of AMPA channel

NEURON {
	POINT_PROCESS pyr2pyr 	: declare pyr2pyr as a point process(applied at point). Others are distributed ones.
	USEION ca READ eca		: declares ca will be used in the model, eca will be treated as a PARAMETER
	NONSPECIFIC_CURRENT inmda, iampa	: This signifies that we are calculating local currents which get added to the total membrane current but will not contribute to any particular ionic concentration.
	RANGE initW		: These names will be become range variables , they are different from parameter as they are displayed in the GUI with range of values that can be varied
	RANGE Cdur_nmda, AlphaTmax_nmda, Beta_nmda, Erev_nmda, gbar_nmda, W_nmda, on_nmda, g_nmda : These names will be become range variables
	RANGE Cdur_ampa, AlphaTmax_ampa, Beta_ampa, Erev_ampa, gbar_ampa, W, on_ampa, g_ampa : These names will be become range variables
	RANGE eca, ICa, P0, fCa, tauCa, iCatotal : These names will be become range variables
	RANGE Cainf, pooldiam, z	: These names will be become range variables
	RANGE lambda1, lambda2, threshold1, threshold2	: These names will be become range variables
	RANGE fmax, fmin, Wmax, Wmin, maxChange, normW, scaleW, srcid, destid	: These names will be become range variables
	RANGE pregid,postgid	: These names will be become range variables
}

UNITS {	: Declares all the units
	(mV) = (millivolt)
    (nA) = (nanoamp)
	(uS) = (microsiemens)
	FARADAY = 96485 (coul)
	pi = 3.141592 (1)
}

PARAMETER {

	srcid = -1 (1)
	destid = -1 (1)
	: Delcaring NMDA parameters 
	Cdur_nmda = 16.7650 (ms)	: duration of [T] , where [T] is a step function which models binding to a neurotransmitter
	AlphaTmax_nmda = .2659 (/ms): forward kinetics constant
	Beta_nmda = 0.008 (/ms)		: backward kinetics constant
	Erev_nmda = 0 (mV)			: Reversal Potential of NMDA
	gbar_nmda = .5e-3 (uS)		: NMDA conductance

	Cdur_ampa = 1.4210 (ms)	: duration of [T] , where [T] is a step function which models binding to a neurotransmitter
	AlphaTmax_ampa = 3.8142 (/ms)	: forward kinetics constant
	Beta_ampa = 0.1429 (/ms)	: backward kinetics constant
	Erev_ampa = 0 (mV)	: Reversal Potential of AMPA
	gbar_ampa = 1e-3 (uS)	: NMDA conductance

	eca = 120	: reversal potential for calcium

	Cainf = 50e-6 (mM)	: steady state calcium concentration
	pooldiam =  1.8172 (micrometer)	: Diameter of Ca pool
	z = 2	: valence of Ca

	tauCa = 50 (ms)		: decay time constant
	P0 = .015	: P0 is the fraction of NMDARs in the closed state that shift to open after presynaptic spike
	fCa = .050 :0.24	: Determines the decay of Ca pool 
	
	lambda1 = 10:80: 20 : 15 :8 :5: 2.5	: Learning parameters
	lambda2 = 0.3 : .01	: Learning parameters
	threshold1 = 0.45 : 0.35 :0.35:0.2 :0.50 (uM)	: LTD Threshold in omega function
	threshold2 = 0.50 : 0.40 :0.4 :0.3 :0.60 (uM)	: LTP Threshold in omega function

	initW = 1 : 2 : 2: 2 : 1 : 10 : 6 :1.5	:Initial Weight of AMPA
	fmax = 1000 : 4 : 2 : 3 : 1.5 : 3	: fmax determines max weight 
	fmin = 0.001	: fmin determines the minimum weight
	
}

ASSIGNED { : variables which can be computed directly by assignment statements
	v (mV) 	: Voltage

	inmda (nA)	: NMDA current
	g_nmda (uS) :	NMDA conductance
	on_nmda	: this is like a flag. It is wither 0 or 1. 
	W_nmda	: Weight of NMDA

	iampa (nA)	: AMPA current
	g_ampa (uS)	: AMPA conductance
	on_ampa	: this is like a flag. It is wither 0 or 1. 
	W	: Weight of AMPA

	t0 (ms)	: time variable

	ICa (mA)	: Calcium current
	Afactor	(mM/ms/nA)	
	iCatotal (mA)

	dW_ampa	: change in AMPA weight
	Wmax	: Maximum weight
	Wmin	: Minimum weight
	maxChange	: max change in weight
	normW	: normalized weight
	scaleW	: scaled weight
	
	pregid	
	postgid
}

STATE { r_nmda r_ampa capoolcon } : They are normally the variables to be "SOLVE"ed for within the BREAKPOINT block

INITIAL {
: The INITIAL block is called when the user executes the finitialize() function from hoc

	on_nmda = 0
	r_nmda = 0
	W_nmda = initW

	on_ampa = 0
	r_ampa = 0
	W = initW

	t0 = -1

	Wmax = fmax*initW	: calculating maximum weight
	Wmin = fmin*initW	: calculating minimum weight
	maxChange = (Wmax-Wmin)/10	: calculating maximum change in weight
	dW_ampa = 0	

	capoolcon = Cainf
	Afactor	= 1/(z*FARADAY*4/3*pi*(pooldiam/2)^3)*(1e6)
}

BREAKPOINT {
	SOLVE release METHOD cnexp
}

DERIVATIVE release {
: this block is used to assign values to the derivatives of the states
 
	if (t0>0) {
		if (t-t0 < Cdur_nmda) {
			on_nmda = 1
		} else {
			on_nmda = 0
		}
		if (t-t0 < Cdur_ampa) {
			on_ampa = 1
		} else {
			on_ampa = 0
		}
	}
	r_nmda' = AlphaTmax_nmda*on_nmda*(1-r_nmda)-Beta_nmda*r_nmda	: Kinectic equation for NMDA 
	r_ampa' = AlphaTmax_ampa*on_ampa*(1-r_ampa)-Beta_ampa*r_ampa	: Kinectic equation for AMPA

	dW_ampa = eta(capoolcon)*(lambda1*omega(capoolcon, threshold1, threshold2)-lambda2*W)*dt : Calcium control hypothesis to implement learning

	: Limit for extreme large weight changes
	if (fabs(dW_ampa) > maxChange) {
		if (dW_ampa < 0) {
			dW_ampa = -1*maxChange
		} else {
			dW_ampa = maxChange
		}
	}

	:Normalize the weight change
	normW = (W-Wmin)/(Wmax-Wmin)
	if (dW_ampa < 0) {
		scaleW = sqrt(fabs(normW))
	} else {
		scaleW = sqrt(fabs(1.0-normW))
	}

	W = W + dW_ampa*scaleW	
	
	:Weight value limits
	if (W > Wmax) { 
		W = Wmax
	} else if (W < Wmin) {
 		W = Wmin
	}

	g_nmda = gbar_nmda*r_nmda
	inmda = W_nmda*g_nmda*(v - Erev_nmda)*sfunc(v) 	: NMDA current equation

	g_ampa = gbar_ampa*r_ampa
	iampa = W*g_ampa*(v - Erev_ampa)	: AMPA current equation

	ICa = P0*g_nmda*(v - eca)*sfunc(v)
	capoolcon'= -fCa*Afactor*ICa + (Cainf-capoolcon)/tauCa	: calcium pool concentration
}

NET_RECEIVE(dummy_weight) {
	t0 = t
}

:::::::::: FUNCTIONs and PROCEDUREs ::::::::::::

FUNCTION sfunc (v (mV)) {
	UNITSOFF
	sfunc = 1/(1+0.33*exp(-0.06*v)) : Magnesium block
	UNITSON
}

FUNCTION eta(Cani (mM)) {
: this block determines the learning rate
	LOCAL taulearn, P1, P2, P4, Cacon
	P1 = 0.1
	P2 = P1*1e-4
	P4 = 1
	Cacon = Cani*1e3
	taulearn = P1/(P2+Cacon*Cacon*Cacon)+P4
	eta = 1/taulearn*0.001
}

FUNCTION omega(Cani (mM), threshold1 (uM), threshold2 (uM)) {
: determines the omega function
	LOCAL r, mid, Cacon
	Cacon = Cani*1e3
	r = (threshold2-threshold1)/2
	mid = (threshold1+threshold2)/2
	if (Cacon <= threshold1) { omega = 0}
	else if (Cacon >= threshold2) {	omega = 1/(1+50*exp(-50*(Cacon-threshold2)))}
	else {omega = -sqrt(r*r-(Cacon-mid)*(Cacon-mid))}
}

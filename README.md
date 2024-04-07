## Enhancing Sequence Model with Mathematical Reasoning in Symbolic Integration

The supplementary materials include: the code for data generation and model training, the implementation of coefficient abstraction, additive decomposition, and out-of-distribution generalization, and the data of experimental results.

## Dataset

We use utilities from the implementation of  Lample \& Charton (2020) to generate datasets. We clone their repo into the folder SymM.

Please execute the following command to generate a dataset:

```bash
python main.py 
--export_data true
--batch_size 32					# batch size
--cpu true						# cpu or gpu
--exp_name data					# experiment name
--num_workers 8					# number of processes
--tasks prim_bwd               	# task (prim_fwd, prim_bwd, prim_ibp, ode1, ode2)
--n_variables 1                	# number of variables (x, y, z)
--n_coefficients 10          	# number of coefficients (a_0, a_1, a_2, ...)
--leaf_probs "0.5,0.5,0,0"   	# leaf sampling probabilities
--max_ops 15                   	# maximum number of operators
--max_int 5                    	# max value of sampled integers
--positive true                	# sign of sampled integers
--max_len 512                  	# maximum length of generated equations
--operators "add:10,sub:3,mul:10,div:5,sqrt:4,pow2:4,pow3:2,pow4:1,pow5:1,ln:4,exp:4,sin:4,cos:4,tan:4,asin:1,acos:1,atan:1,sinh:1,cosh:1,tanh:1,asinh:1,acosh:1,atanh:1"
```

Then you can split it to training, validation, and test set respectively.

## Model

Once you have a training / validation / test set, you can train our model using the following command:

```bash
python main.py
--exp_name first_train  				# experiment name
--fp16 true --amp 2     				# float16 training
--tasks "prim_bwd"                    	# task
--reload_data "prim_bwd,prim_bwd.train,prim_bwd.valid,prim_bwd.test"  # data location
--reload_size 10000000                  # training set size
--emb_dim 1024    						# model dimension
--n_enc_layers 6  						# encoder layers
--n_dec_layers 6  						# decoder layers
--n_heads 8       						# number of heads
--optimizer "adam,lr=0.0001"       		# model optimizer
--batch_size 32                 		# batch size
--epoch_size 50000             			# epoch size (number of equations per epoch)
```

## Robustness Test

Generate the test dataset for robustness:

```bash
python admath/robustness.py 
--output-dir ./output 						# output path
--model-path bwd.pth 						# model path
--symbolic-math-repo-path ../SymM 			# code path
--exprs 'simple_coeff1_range' 				# mode
--N 1000									# number of expressions
--top-n 10									# beam size
```

Then you can check and verify:

```bash
python admath/verify.py 
--generations simple_coeff1.json 			# data path
--method sympy 								# method
--early-stop   								# early stop
--output-dir ./output 						# output path
--symbolic-math-repo-path ../SymM 			# code path
--top-n 10									# beam size
```

The comparison results between our model and LC model are saved in Experiment/robustness.

# Compositionality Test

Generate the test dataset for compositionality:

```bash
python admath/compositionality.py 
--output-dir ./output										# output path 
--generations-file 'simple_coeff1_verified_sympy_top10.json' 		# reference
--model-path bwd.pth 										# model path
--symbolic-math-repo-path ../SymM 							# code path
--N 1000 													# number of expressions
--top-n 10													# beam size
```

Then do the "check and verify" step above.

The comparison results between our model and LC model are saved in Experiment/compositionality.

## Out-of-distribution Generalization Test

You can run Rosymtor/out.py to execute the mathematical substitution. 

## SAGGA Test

Execute the following command to find the counterexample of our model by SAGGA:

```bash
python admath/genetic.py --basis polynomial --fitness-type length_penalty
```

In our experiment, we test for two hours and get a Timeout result.
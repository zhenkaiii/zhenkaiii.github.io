def mse_loss(pred, target):
	"""
	pred: B, S, D
	target: B, S, D

	return (1,)
	"""
	return ((pred-target)**2).mean(dim=None)


# def softmax(logit):
# 	"""
# 	logit: B, S, D

# 	return: B, S, D
# 	"""

# 	nom = torch.exp(logit) # there's no torch.pow! # torch.exp is purely element-wise, no dim!
# 	denom = nom.sum(dim=-1, keepdim=True)
# 	return nom/denom


def softmax(logit):
	"""
	e**x_j / sum(e**x_i)
	
	logit: B, S, D
	return: B, S, D
	"""

	logit = logit - logit.max(dim=-1, keepdim=True).values
	nom = torch.exp(logit) # torch.exp is purely element-wise, no dim!
	denom = nom.sum(dim=-1, keepdim=True)
	return nom / denom




def xentropy(logit, label):
	"""
	logit: B, S, D
	label: B, S
	return: B, S
	"""
	B, S, _ = logit.size()
	# right_logit = logit[torch.arange(B), torch.arange(S), label] # B, S
	right_logit = torch.gather(logit, dim=-1, index=label.unsqueeze(-1)).squeeze(-1)
	return torch.logsumexp(logit, dim=-1) - right_logit # B, S




def rmsnorm(x, gamma):
	"""
	x: b, s, d
	gamma: d,
	"""

	# x = x/torch.sqrt(x, dim=-1, keepdim=True) # is purely element-wise, no dim!
	x_rms = (x**2).mean(dim=-1, keepdim=True).sqrt()	
	return (x/x_rms)*gamma
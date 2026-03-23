import torch
import torch.nn as nn
import torch.nn.functional as F # lower single case

class MiniTransformerBlock(nn.Module):
	def __init__(self, d_model, d_ff, n_head):
		# alwasy first line when init for nn.Module. burn it in!
		super().__init__()
		self.mha = nn.MultiheadAttention(d_model, n_head)
		# Sequential links dense + act + dense. burn it in!
		self.mlp = nn.Sequential(
			nn.Linear(d_model, d_ff),
			nn.SiLU(),
			nn.Linear(d_ff, d_model),
			)
		# one norm for each! and rms must be self implemnted as there's no off-the-shelf one.
		self.norm_1 = nn.LayerNorm(d_model)
		self.norm_2 = nn.LayerNorm(d_model)

	def forward(self, x):
		norm_1_x = self.norm_1(x)
		mha_x, _ = self.mha(norm_1_x, norm_1_x, norm_1_x) # self attention but you need to feed q k v separately to tell it's self attention! 
		mha_x_res_added = x + mha_x # residul 1
		norm_2_x = self.norm_2(mha_x_res_added)
		mlp_x = self.mlp(norm_2_x)
		return mha_x_res_added + mlp_x # residual 2. # there're 2 residuals, non is from original x to the very end!


# (B, S, D): 32, 128, 4096

# YOU JUST NEED data model op, these 3 before training loop! no loss!
# USE PYTORCH! 
random_data = torch.randn(32, 128, 4096)
model = MiniTransformerBlock(4096, 16384, 16)
op = torch.optim.Adam(model.parameters(), lr = 1e-3)


for i in range(20):
	# you will need 2 optimizer ops and two loss ops - o-l-l-o. backward is for loss, step is for op!
	op.zero_grad() # Clears the gradients from the previous step to disable grad accumulation!
	selected_batch = torch.randint(0, 32, (4,)) # torch.randint needs a tuple for size
	trn_x = random_data[selected_batch]

	trn_y = trn_x[:, 1:, :] # "next" shift is on token 
	pred = model(trn_x[:,:-1,:]) # give up on last or shape won't match.

	loss = F.mse_loss(pred, trn_y)
	loss.backward()
	op.step()


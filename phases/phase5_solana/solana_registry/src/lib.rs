use anchor_lang::prelude::*;

declare_id!("KeyRegistry11111111111111111111111111111");

#[program]
pub mod key_registry {
    use super::*;

    // Register the caller's Ed25519 public key.
    pub fn register_key(ctx: Context<RegisterKey>, public_key: [u8; 32]) -> Result<()> {
        let key_record = &mut ctx.accounts.key_record;
        key_record.owner = ctx.accounts.owner.key();
        key_record.public_key = public_key;
        key_record.bump = ctx.bumps.key_record;
        
        msg!("Registered public key for user: {}", ctx.accounts.owner.key());
        msg!("Public key (hex): {:02x?}", public_key);
        
        Ok(())
    }

    // Update the caller's registered Ed25519 public key.
    pub fn update_key(ctx: Context<UpdateKey>, new_public_key: [u8; 32]) -> Result<()> {
        let key_record = &mut ctx.accounts.key_record;
        
        // Only the owner can update
        require_keys_eq!(
            key_record.owner,
            ctx.accounts.owner.key(),
            KeyRegistryError::Unauthorized
        );
        
        key_record.public_key = new_public_key;
        
        msg!("Updated public key for user: {}", ctx.accounts.owner.key());
        msg!("New public key (hex): {:02x?}", new_public_key);
        
        Ok(())
    }

    // Check whether `public_key_to_verify` matches the stored key.
    pub fn verify_key(ctx: Context<VerifyKey>, public_key_to_verify: [u8; 32]) -> Result<bool> {
        let key_record = &ctx.accounts.key_record;
        let matches = key_record.public_key == public_key_to_verify;
        
        if matches {
            msg!("✅ Public key matches registered key for user: {}", key_record.owner);
        } else {
            msg!("❌ Public key does NOT match registered key for user: {}", key_record.owner);
        }
        
        Ok(matches)
    }
}

#[derive(Accounts)]
#[instruction(public_key: [u8; 32])]
pub struct RegisterKey<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    
    #[account(
        init,
        payer = owner,
        space = 8 + KeyRecord::LEN,
        seeds = [b"key_record", owner.key().as_ref()],
        bump
    )]
    pub key_record: Account<'info, KeyRecord>,
    
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(new_public_key: [u8; 32])]
pub struct UpdateKey<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    
    #[account(
        mut,
        seeds = [b"key_record", owner.key().as_ref()],
        bump = key_record.bump,
        has_one = owner @ KeyRegistryError::Unauthorized
    )]
    pub key_record: Account<'info, KeyRecord>,
}

#[derive(Accounts)]
#[instruction(public_key_to_verify: [u8; 32])]
pub struct VerifyKey<'info> {
    #[account(
        seeds = [b"key_record", key_record.owner.as_ref()],
        bump = key_record.bump
    )]
    pub key_record: Account<'info, KeyRecord>,
}

#[account]
pub struct KeyRecord {
    pub owner: Pubkey,        // wallet address
    pub public_key: [u8; 32], // Ed25519 public key
    pub bump: u8,             // PDA bump
}

impl KeyRecord {
    pub const LEN: usize = 32 + 32 + 1; // owner + public_key + bump
}

#[error_code]
pub enum KeyRegistryError {
    #[msg("Unauthorized: You are not the owner of this key record")]
    Unauthorized,
}




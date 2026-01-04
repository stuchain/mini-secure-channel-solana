// Program entrypoint (demo)
use anchor_lang::prelude::*;

declare_id!("KeyRegistry11111111111111111111111111111");

#[program]
pub mod key_registry {
    use super::*;
    
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}




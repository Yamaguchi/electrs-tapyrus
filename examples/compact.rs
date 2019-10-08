/// Benchmark full compaction.
extern crate electrs_tapyrus;

#[macro_use]
extern crate log;

extern crate error_chain;

use electrs_tapyrus::{config::Config, errors::*, store::DBStore};

use error_chain::ChainedError;

fn run(config: Config) -> Result<()> {
    if !config.db_path.exists() {
        panic!(
            "DB {:?} must exist when running this benchmark!",
            config.db_path
        );
    }
    let store = DBStore::open(&config.db_path, /*low_memory=*/ true);
    store.compact();
    Ok(())
}

fn main() {
    if let Err(e) = run(Config::from_args()) {
        error!("{}", e.display_chain());
    }
}

" Setup leader
let mapleader = "\<Space>"
map <leader>u :u<CR>
map <leader>h :noh<CR>
map <leader># 78<S-I>#<Esc>o<Esc>
map <leader>o o<Esc>
map <leader>O O<Esc>
map <leader>t :set expandtab<CR>
map <leader>T :set noexpandtab<CR>
set showcmd
set timeoutlen=500

" Make switch to NORMAL mode more responsive
set ttimeoutlen=5

" Tabbing
set autoindent
set smartindent
set tabstop=4
set shiftwidth=4

" Enable line numbers with room to spare
set number
set numberwidth=6

" Hard wrap at 80 columns
set textwidth=78
set colorcolumn=79

" Enable changing lines when moving beyond the beginning/end of the current line
set whichwrap+=<,>,h,l,[,]

" Always use syntax highlighting
syntax on

" Enable highlight while searching
set hlsearch

" Display unprintable characters
set list
set listchars=tab:⋮\ ,trail:•,extends:»,precedes:«


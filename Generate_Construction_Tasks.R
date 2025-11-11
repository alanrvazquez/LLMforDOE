library(FrF2)
source("DoE_functions.R")

# Define elements of the prompt
role = "You are an expert in the subfield of statistics called design of experiments"
goal = "Your goal is to construct a two-level fractional factorial design with maximum resolution and minimum aberration"
levels_context = "The factors have two levels coded as '-1' and '+1'"
template = "You will only generate a table containing the design. You will not generate any text explaining the table or your answer"
format.template = "The table must be in a comma-separated values (CSV) format. Specifically, the values in the table must be separated by ‘,’ and each row must end with ‘\\\\’. In the table, the first row will be used as a header row to count the factors starting at ‘1’. The first column will be called “Run” and used to count the number of runs starting at ‘1’. Each design cell (excluding the header and Run columns) must contain either ‘-1’ or ‘1’" 

n = 32 
k.start = log2(n) + 1
name_instruction_set = paste("instructions/instruction_dataset_n", n, ".json", sep = '')
designs = list()
resolutions = list()
MomentAberration = list()
ClearINTs = list()
prompts = list()

citer = 1
for (k in k.start:(n-1)){
  
  # Create prompt.
  size_context = paste("The number of factors is", k, "and the number of runs is", n)
  instruction = paste("Construct the two-level fractional factorial design with", n, "runs and", k, "factors that has maximum resolution and minimum aberration.")
  
  p = paste(role, goal, size_context, levels_context, template, 
            format.template, instruction, sep = ". ")
  
  # save prompt.
  prompts[[citer]] = p
  
  # Generate design.
  my.design = FrF2(nruns = n, nfactors = k)
  my.design.info = design.info(my.design)
  
  # Save designs.
  D = desnum(my.design)
  designs[[citer]] = D
  
  # Save design properties.
  resolutions[[citer]] = res(my.design.info$catlg.entry)
  ClearINTs[[citer]] = nclear.2fis(my.design.info$catlg.entry)
  
  MomentAberration[[citer]] = list("a" = moment_aberration(D))
  
  citer = citer + 1
}



# Generate individual instructions.
each.instruction = list()
for (ii in 1:length(designs)){
  output.ID = paste('"ID":', ii)
  output.N = paste('"N":', n)
  output.prompt = paste('"prompt":', paste('"', prompts[[ii]], '"', sep = ''))
  output.clearint = paste('"clearIteractions":', ClearINTs[[ii]])
  output.res = paste('"resolution":', resolutions[[ii]])
  MAtext = paste("[", paste(MomentAberration[[ii]]$a, collapse = ","), "]", sep = "")
  output.momentaberration = paste('"MomentAberrationPattern":', MAtext)
  single.instruction = paste(output.ID, output.N, output.prompt, output.res, output.clearint, 
                            output.momentaberration, sep = ',')
  each.instruction[[ii]] = paste("{", single.instruction, "}", sep = '')
}

# Compile all instructions
all.instructions = paste(each.instruction, collapse = ',')
all.instructions = paste('[', all.instructions, ']', sep = '')

writeLines(all.instructions, name_instruction_set)


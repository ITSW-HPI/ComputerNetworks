# ComputerNetworks
Material for a Bachelor-level lecture on Computer Networks 

The target audience is a third-year Computer Science Bachelor class,
with 6 LP/ECTS. Subsets shold be easily useable for a shorter (e.g., 4
ECTS class). 

## Material, preparation 

Material will be produced using emacs org mode, from which LaTeX
Beamer files will be generated. These can be turned into slides as
well as handout scripts. 

You need emacs and and org-mode v9 or better. Adapt path name for the
emacs executable in Makefile. 


## TODO 

- describe how to add material, compile into PDFs 

- currently based on a template hpi-slides, but that uses a proprietary font that cannot be shared in a public repo. We need to find a version with free fonts; ideally a branch structure that can incorporate different slide layouts 

### Convenient latexmk replacement 

fswatch -o *.org figures/*.tex  | xargs  -n1 make slides

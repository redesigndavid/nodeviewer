import sys
from PyQt4.QtGui import QApplication
from node_viewer import NodeViewer
from node_viewer import style
import random


_random_titles = [item.strip() for item in """
Citizen Kane
Vertigo
2001: A Space Odyssey
Rules Of The Game, The
Tokyo Story
Godfather, The
Sunrise
Searchers, The
Seven Samurai
Apocalypse Now
Singin' In The Rain
Battleship Potemkin
Bicycle Thieves
Taxi Driver
Passion Of Joan Of Arc, The
Breathless
Atalante, L'
Persona
Man With A Movie Camera
Rashomon
Godfather Part Ii, The
Raging Bull
Andrei Rublev
400 Blows, The
Psycho
City Lights
Touch Of Evil
Mirror, The
Dolce Vita, La
Some Like It Hot
Lawrence Of Arabia
Ordet
Au Hasard Balthazar
Casablanca
Avventura, L'
General, The
Contempt
Sunset Blvd.
Blade Runner
Rear Window
Grande Illusion, La
Night Of The Hunter, The
Third Man, The
In The Mood For Love
Fanny And Alexander
Ugetsu Monogatari
Modern Times
Chinatown
Playtime
Barry Lyndon
M
Dr. Strangelove Or: How I Learned To Stop Worrying And Love The Bomb
Metropolis
Wild Strawberries
Apartment, The
Pather Panchali
Enfants Du Paradis, Les
Stalker
North By Northwest
Shoah
Rio Bravo
Magnificent Ambersons, The
Mulholland Dr.
Wild Bunch, The
Battle Of Algiers, The
Pierrot Le Fou
Once Upon A Time In The West
Gold Rush, The
Seventh Seal, The
Voyage In Italy
Amarcord
Strada, La
Late Spring
Leopard, The
Pickpocket
Blue Velvet
Goodfellas
Conformist, The
Pulp Fiction
Viridiana
Jules Et Jim
Gertrud
Nashville
It'S A Wonderful Life
Clockwork Orange, A
Man Escaped, A
Greed
Man Who Shot Liberty Valance, The
Close-Up
Annie Hall
Aguirre: The Wrath Of God
Sansho The Bailiff
Last Year At Marienbad
Jaws
Shining, The
Sans Soleil
Jeanne Dielman, 23 Quai Du Commerce, 1080 Bruxelles
Intolerance
Blowup
Mother And The Whore, The
To Be Or Not To Be
Wizard Of Oz, The
Gone With The Wind
Eclisse, L'
Woman Under The Influence, A
Once Upon A Time In America
Manhattan
Sherlock Jr.
Ikiru
Letter From An Unknown Woman
Star Wars
Madame De...
All About Eve
Hiroshima Mon Amour
One Flew Over The Cuckoo'S Nest
My Darling Clementine
Notorious
Bringing Up Baby
Brighter Summer Day, A
Olvidados, Los
Nosferatu
Don'T Look Now
Badlands
Vivre Sa Vie
Spirit Of The Beehive, The
Partie De Campagne
Yi Yi
Rome, Open City
Matter Of Life And Death, A
E.T. The Extra-Terrestrial
Chien Andalou, Un
Lady Eve, The
Ali: Fear Eats The Soul
Trouble In Paradise
Days Of Heaven
Do The Right Thing
Stagecoach
Exterminating Angel, The
Alien
Double Indemnity
His Girl Friday
Come And See
Conversation, The
Brief Encounter
On The Waterfront
Gospel According To St. Matthew, The
Discreet Charm Of The Bourgeoisie, The
Chimes At Midnight
Rosemary'S Baby
Beau Travail
King Kong
Red Shoes, The
River, The
Cries And Whispers
Good, The Bad And The Ugly, The
Duck Soup
Passenger, The
Life And Death Of Colonel Blimp, The
Argent, L'
Grapes Of Wrath, The
Mouchette
Imitation Of Life
Deer Hunter, The
Black Narcissus
Dekalog
Travelling Players, The
Umbrellas Of Cherbourg, The
Spring In A Small Town
Earth
Brazil
Celine And Julie Go Boating
Performance
Last Laugh, The
Rocco And His Brothers
Ran
Out Of The Past
Great Dictator, The
There Will Be Blood
Best Years Of Our Lives, The
Night And Fog
Mccabe & Mrs. Miller
Sweet Smell Of Success
Umberto D.
Death In Venice
Quiet Man, The
Red River
Paisan
Kes
Close Encounters Of The Third Kind
Belle De Jour
Breaking The Waves
Birds, The
Nanook Of The North
Nights Of Cabiria
City Of Sadness, A
Two Or Three Things I Know About Her
Wavelength
Ashes And Diamonds
Vampyr
Spirited Away
Thin Red Line, The
Piano, The
Cabinet Of Dr. Caligari, The
Meet Me In St. Louis
Schindler'S List
Kind Hearts And Coronets
Sullivan'S Travels
Fargo
Ivan The Terrible, Part 2
Chungking Express
Texas Chainsaw Massacre, The
Crowd, The
Diary Of A Country Priest
Colour Of Pomegranate, The
Only Angels Have Wings
Raiders Of The Lost Ark
Graduate, The
Mean Streets
Life Of Oharu, The
Exorcist, The
Tabu
Germany, Year Zero
Bonnie And Clyde
Treasure Of The Sierra Madre, The
Solaris
Tree Of Life, The
Wings Of Desire
Band Wagon, The
Shop Around The Corner, The
Meshes Of The Afternoon
Johnny Guitar
Tropical Malady
Notte, La
Thin Blue Line, The
Unforgiven
Groundhog Day
My Night At Maud'S
Three Colours: Red
Zero For Conduct
Paris, Texas
Night Of The Living Dead
Eternal Sunshine Of The Spotless Mind
Crimes And Misdemeanors
Ivan The Terrible, Part 1
My Neighbour Totoro
Three Colours: Blue
Floating Clouds
Paths Of Glory
Distant Voices, Still Lives
Magnolia
Story Of The Last Chrysanthemums, The
Broken Blossoms
Pandora'S Box
Verdugo, El
Big Lebowski, The
Freaks
Throne Of Blood
Birth Of A Nation, The
F For Fake
Week-End
In A Lonely Place
Music Room, The
Black God, White Devil
Monsieur Verdoux
Faces
Maltese Falcon, The
Memories Of Underdevelopment
Wages Of Fear, The
World Of Apu, The
Eraserhead
Day Of Wrath
Big Sleep, The
Underground
Love Streams
Husbands
Canterbury Tale, A
Autumn Afternoon, An
Touki Bouki
Kings Of The Road
Orpheus
Philadelphia Story, The
Cinema Paradiso
Listen To Britain
Videodrome
Berlin Alexanderplatz
Puppetmaster, The
Last Picture Show, The
Reservoir Dogs
Harold And Maude
To Kill A Mockingbird
Peeping Tom
Empire Strikes Back, The
Mr. Hulot'S Holiday
Sacrifice, The
All About My Mother
Bride Of Frankenstein
In The Realm Of The Senses
Amadeus
Crime Of Monsieur Lange, The
Killer Of Sheep
Marnie
Matrix, The
Thing, The
Cabaret
October
Killing Of A Chinese Bookie, The
Dawn Of The Dead
Werckmeister Harmonies
El
Written On The Wind
Time To Live And The Time To Die, The
It Happened One Night
Midnight Cowboy
I Am Cuba
Kid, The
Dog Day Afternoon
Red Desert
Touch Of Zen, A
Make Way For Tomorrow
Eyes Wide Shut
West Side Story
Eyes Without A Face
Where Is The Friend'S Home?
City Of God
Back To The Future
Happy Together
How Green Was My Valley
Through The Olive Trees
Snow White And The Seven Dwarfs
Shoot The Piano Player
Tie Xi Qu: West Of The Tracks
Kiss Me Deadly
Lost Highway
Days Of Being Wild
Russian Ark
I Was Born, But...
Don'T Look Back
Green Ray, The
Voyage Dans La Lune, Le
Salvatore Giuliano
Affair To Remember, An
Festen
Palm Beach Story, The
Bridge On The River Kwai, The
Last Tango In Paris
This Is Spinal Tap
King Of Comedy, The
Double Life Of Veronique, The
Tenant, The
1900
In A Year With 13 Moons
Woman In The Dunes
Chelsea Girls
Man Of Aran
Heat
I Know Where I'M Going!
Network
Nostalghia
Butch Cassidy And The Sundance Kid
All That Heaven Allows
Yojimbo
Landscape In The Mist
Cloud-Capped Star, The
Moment Of Innocence, A
Tree Of Wooden Clogs, The
Star Is Born, A
Shadows
Dead Ringers
High And Low
Wanda
Young Girls Of Rochefort, The
Stranger Than Paradise
Out 1, Noli Me Tangere
Ivan'S Childhood
Stromboli
Charulata
Silence Of The Lambs, The
Closely Watched Trains
French Cancan
High Noon
Dead, The
Brokeback Mountain
Hustler, The
Wall-E
Teorema
Gleaners & I, The
Plaisir, Le
Carrie
Hour Of The Furnaces, The
Koyaanisqatsi
To Have And Have Not
Opening Night
Raise The Red Lantern
Five Easy Pieces
Heaven'S Gate
Sorrow And The Pity, The
Uncle Boonmee Who Can Recall His Past Lives
Daisies
Dogville
House Is Black, The
Tristana
Taste Of Cherry
Aliens
Pyaasa
Army Of Shadows
Masculin Feminin
Barren Lives
Fitzcarraldo
Scenes From A Marriage
Long Goodbye, The
Terra Em Transe
Cameraman, The
Turin Horse, The
Death Of Mr. Lazarescu, The
Kagemusha
Fight Club
Awful Truth, The
Quince Tree Of The Sun
Hour Of The Wolf
Innocents, The
White Ribbon, The
Alexander Nevsky
Gimme Shelter
Scarlet Empress, The
Wind Will Carry Us, The
Limelight
Suspiria
Senso
Day For Night
Easy Rider
Shawshank Redemption, The
Night At The Opera, A
Platform
Enigma Of Kaspar Hauser, The
Elephant
Chronicle Of A Summer
Some Came Running
Dersu Uzala
Short Cuts
Strangers On A Train
Wind, The
Shane
Fantasia
Triumph Of The Will
Monty Python'S Life Of Brian
Early Summer
Shadows Of Our Forgotten Ancestors
Elephant Man, The
Mad Max 2
Muriel
Punch-Drunk Love
Terminator, The
Pinocchio
Toy Story
Naked
Top Hat
Lady From Shanghai, The
Two-Lane Blacktop
Sound Of Music, The
Silence, The
Land Without Bread
Crouching Tiger, Hidden Dragon
Point Blank
Grey Gardens
Flowers Of St. Francis, The
Forrest Gump
Flowers Of Shanghai
Lola
Yellow Earth
Melancholia
Hoop Dreams
Steamboat Bill, Jr.
India Song
Repulsion
Cranes Are Flying, The
Mon Oncle
Winter Light
Tale Of Tales
Wedding March, The
Miracle In Milan
Talk To Her
Withnail & I
Safe
All That Jazz
Barton Fink
Loves Of A Blonde
Vampires, Les
Wagon Master
Dead Man
Terra Trema, La
Frankenstein
Alphaville
Lives Of Others, The
Halloween
Our Hospitality
Tootsie
All The President'S Men
Casino
Cat People
Servant, The
Devils, The
Bigger Than Life
Providence
Phantom Of Liberty, The
Doctor Zhivago
Faust
Rise To Power Of Louis Xiv, The
Damned, The
Ninotchka
Trainspotting
Rebel Without A Cause
Aparajito
Big Heat, The
Down By Law
Hannah And Her Sisters
Picnic At Hanging Rock
Farewell, My Concubine
Alice In The Cities
Shadow Of A Doubt
12 Angry Men
Pat Garrett And Billy The Kid
Laura
Asphalt Jungle, The
Accattone
Hard Day'S Night, A
Oldboy
Rosetta
East Of Eden
Boogie Nights
That Obscure Object Of Desire
Bitter Tears Of Petra Von Kant, The
Colossal Youth
Separation, A
Scorpio Rising
Bring Me The Head Of Alfredo Garcia
Vitelloni, I
Salesman
Walkabout
Boudu Saved From Drowning
Secrets & Lies
Great Expectations
Fellini Satyricon
Detour
Deliverance
No Country For Old Men
Being There
Grizzly Man
Local Hero
Lost In Translation
Blue Angel, The
My Own Private Idaho
Lady Vanishes, The
Dr. Mabuse, The Gambler
French Connection, The
Full Metal Jacket
Love Me Tonight
A.I. Artificial Intelligence
Inland Empire
Rocky
Strike
Ben-Hur
I Walked With A Zombie
Red Circle, The
Splendor In The Grass
Devil, Probably, The
Hana-Bi
In Vanda'S Room
Scarface
Die Hard
Raising Arizona
Antonio Das Mortes
Goodbye, Dragon Inn
Tiger Of Eschnapur, The
Royal Tenenbaums, The
Xala
Titicut Follies
Rebecca
Songs From The Second Floor
Blissfully Yours
Place In The Sun, A
Funny Games
Age Of Innocence, The
Silent Light
Killing, The
Mother And Son
African Queen, The
Round-Up, The
Amants Du Pont-Neuf, Les
Young Frankenstein
Memento
Fat City
Dames Du Bois De Boulogne, Les
Foolish Wives
Yeelen
Lancelot Du Lac
Manchurian Candidate, The
Pan'S Labyrinth
Edvard Munch
By The Bluest Of Seas
Breakfast At Tiffany'S
Passion
Man Who Would Be King, The
Nostalgia For The Light
Young Mr. Lincoln
Chant D'Amour, Un
Dazed And Confused
Gummo
39 Steps, The
Requiem For A Dream
They Live By Night
Scarface
And Life Goes On...
Evil Dead Ii
Party, The
Claire'S Knee
My Life As A Dog
Wild Child, The
Emperor'S Naked Army Marches On, The
Before Sunset
Short Film About Killing, A
Rushmore
Belle Noiseuse, La
Purple Rose Of Cairo, The
Dancer In The Dark
Edward Scissorhands
Orlando
Zodiac
Terminator 2: Judgment Day
Distant
Europa '51
Navigator, The
Nouvelle Vague
W.R.: Mysteries Of The Organism
Son, The
Mr. Smith Goes To Washington
Fellini'S Roma
Harlan County, U.S.A.
Hatari!
Limite
Great Escape, The
Miller'S Crossing
Thelma & Louise
White Heat
Se7En
Vive L'Amour
Bambi
Casque D'Or
Flaming Creatures
Seasons, The
Zelig
Woman Next Door, The
Still Life
Seven Chances
Angel At My Table, An
Synecdoche, New York
Faster, Pussycat! Kill! Kill!
Saturday Night And Sunday Morning
Tin Drum, The
Monty Python And The Holy Grail
Marriage Of Maria Braun, The
Dark Knight, The
Red Balloon, The
Spartacus
Ascent, The
Robocop
Red Sorghum
Fly, The
All Quiet On The Western Front
Harakiri
Streetcar Named Desire, A
My Friend Ivan Lapshin
Killer, The
4 Months, 3 Weeks And 2 Days
Wicker Man, The
Crash
Invasion Of The Body Snatchers
Time Of The Gypsies
Idiots, The
Blood Simple
JFK
After Life
Ferris Bueller'S Day Off
Testament Of Dr. Mabuse, The
Lolita
Smiles Of A Summer Night
Holy Mountain, The
Haine, La
Thief Of Bagdad, The
Shock Corridor
Bad And The Beautiful, The
Chronicle Of Anna Magdalena Bach, The
Vengeance Is Mine
Circus, The
Olympia
L.A. Confidential
Misfits, The
Moonfleet
She Wore A Yellow Ribbon
Woman Of Paris, A
Code Unknown
Syndromes And A Century
Arrebato
Hitler: A Film From Germany
Hunger
Port Of Shadows
Possession
Virgin Spring, The
Titanic
Seven Women
Starship Troopers
Blue
Crumb
Gun Crazy
Sauve Qui Peut (La Vie)
Ace In The Hole
Amour
Van Gogh
Producers, The
They Were Expendable
Blow Out
Ossessione
Spione
Dodes'Ka-Den
Moulin Rouge!
Burnt By The Sun
Lusty Men, The
Z
Ludwig
Right Stuff, The
Avatar
Kaagaz Ke Phool
Grido, Il
Headless Woman, The
Au Revoir Les Enfants
Dog Star Man
Trial, The
Last Detail, The
Commune (Paris, 1871), La
Who'S Afraid Of Virginia Woolf?
Diaboliques, Les
Twenty Years Later
Forbidden Games
Long Day Closes, The
Miracle Of Morgan'S Creek, The
Piano Teacher, The
Lord Of The Rings: The Fellowship Of The Ring, The
Cool Hand Luke
Vagabond
American In Paris, An
Morocco
O Lucky Man!
New World, The
Dumbo
Golden Coach, The
Seventh Heaven
River, The
Ghost And Mrs. Muir, The
Pink Flamingos
Taipei Story
Ladykillers, The
Sideways
Fires Were Started
Last Temptation Of Christ, The
End Of Summer, The
Audition
Wild At Heart
Branded To Kill
Akira
Chienne, La
Anatomy Of A Murder
Princess Bride, The
History Of Violence, A
Sun Shines Bright, The
Million, Le
Sur, El
Saturday Night Fever
Sicilia!
Abraham'S Valley
Hart Of London, The
Street Angel
American Beauty
Last Emperor, The
Henry V
Breakfast Club, The
2046
American Graffiti
Cul-De-Sac
Knife In The Water
Mother India
Dust In The Wind
Princess Mononoke
Sweet Hereafter, The
Odd Man Out
Excalibur
We All Loved Each Other So Much
Topsy-Turvy
Intruder, The
Age Of The Earth, The
Fort Apache
Ladies Man, The
Dirty Harry
Blazing Saddles
Last Bolshevik, The
Wings Of Eagles, The
Rififi
Get Carter
Posto, Il
Host, The
Black Orpheus
Grave Of The Fireflies
Veronika Voss
Gilda
Black Girl
Night Of The Demon
Juliet Of The Spirits
Gregory'S Girl
New York, New York
It'S A Gift
On The Town
Angel
Tale Of The Wind, A
Enfant Secret, L'
Pakeezah
My Little Loves
Not Reconciled
Othello
Arabian Nights
Reds
Empire
News From Home
Assault On Precinct 13
Two English Girls
D'Est
Million Dollar Baby
Rope
Simon Of The Desert
Exotica
Street Of Shame
Adventures Of Robin Hood, The
3 Women
Blues Brothers, The
Louisiana Story
Hawks And The Sparrows, The
Criminal Life Of Archibaldo De La Cruz, The
Nuit Du Carrefour, La
Pickup On South Street
Diary For Timothy, A
Diaries, Notes And Sketches
Forbidden Planet
Bob Le Flambeur
Firemen'S Ball, The
Duel In The Sun
Big Deal On Madonna Street
Moi, Un Noir
Usual Suspects, The
Airplane!
National Lampoon'S Animal House
Too Early, Too Late
Love And Death
Reckless Moment, The
Floating Weeds
Ten Commandments, The
To Live
Enfance Nue, L'
Near Dark
Bonheur, Le
47 Ronin, The
As I Was Moving Ahead Occasionally I Saw Brief Glimpses Of Beauty
Ride The High Country
Day The Earth Stood Still, The
Loneliness Of The Long Distance Runner, The
Cairo Station
Elephant
Yol
Ballad Of Narayama, The
Anatahan
Sawdust And Tinsel
Roman Holiday
Subarnarekha
Midnight Run
Match Factory Girl, The
Ice Storm, The
Women On The Verge Of A Nervous Breakdown
India: Matri Bhumi
War And Peace
Fellini'S Casanova
Once Upon A Time In Anatolia
Topo, El
From The Clouds To The Resistance
Berlin: Symphony Of A Great City
Outer Space
Atanarjuat: The Fast Runner
Saragossa Manuscript, The
Lord Of The Rings: The Return Of The King, The
Man Who Fell To Earth, The
El Dorado
42Nd Street
Finding Nemo
Naked Island, The
Grin Without A Cat, A
Shanghai Express
Mothlight
Indian Tomb, The
Princess Yang Kwei Fei
Mildred Pierce
Gentlemen Prefer Blondes
Chikamatsu Monogatari
Ed Wood
Deep End
Holiday
Fata Morgana
Hellzapoppin'
Heimat
Ceddo
Sting, The
Witness
Rocky Horror Picture Show, The
Sonatine
Lone Star
Second Breath
M*A*S*H
Outlaw Josey Wales, The
Central Station
Godfather Part Iii, The
Strangers When We Meet
Ten
Incredible Shrinking Man, The
Zabriskie Point
Unsere Afrikareise
Dracula
Blood Of A Poet, The
Scarecrow
Twin Peaks: Fire Walk With Me
Sweet Sweetback'S Baadasssss Song
Bad Timing
Three Colours: White
Act Of Seeing With One'S Own Eyes, The
Rose Hobart
Tales Of Hoffmann, The
Ju Dou
Yellow Submarine
Femme Est Une Femme, Une
Touchez Pas Au Grisbi
Docks Of New York, The
Broadway Danny Rose
True Heart Susie
Argent, L'
Oedipus Rex
Nightmare Before Christmas, The
America, America
Stardust Memories
Bridges Of Madison County, The
Tarnished Angels, The
Trou, Le
Boot, Das
Storm Over Asia
Dead Poets Society
Outskirts
Fallen Idol, The
When A Woman Ascends The Stairs
Oasis
Go-Between, The
Amour Fou, L'
Happiness
Straight Story, The
Back to the Future
Desperado
Night at the Museum
Robocop
Ghostbusters
Cool World
Donnie Darko
Double Indemnity
The Spanish Prisoner
The Smurfs
Dead Alive
Army of Darkness
Peter Pan
The Jungle Story
Red Planet
Deep Impact
The Long Kiss Goodnight
Juno
(500) Days of Summer
The Dark Knight
Bringing Down the House
Se7en
Chocolat
The American
The American President
Hudsucker Proxy
Conan the Barbarian
Shrek
The Fox and the Hound
Lock, Stock, and Two Barrels
Date Night
200 Cigarettes
9 1/2 Weeks
Iron Man 2
Tombstone
Young Guns
Fight Club
The Cell
The Unborn
Black Christmas
The Change-Up
The Last of the Mohicans
Shutter Island
Ronin
Ocean's 11
Philadelphia
Chariots of Fire
M*A*S*H
Walking and Talking
Walking Tall
The 40 Year Old Virgin
Superman III
The Hour
The Slums of Beverly Hills
Secretary
Secretariat
Pretty Woman
Sleepless in Seattle
The Iron Mask
Smoke
Schindler's List
The Beverly Hillbillies
The Ugly Truth
Bounty Hunter
Say Anything
8 Seconds
Metropolis
Indiana Jones and the Temple of Doom
Kramer vs. Kramer
The Manchurian Candidate
Raging Bull
Heat
About Schmidt
Re-Animator
Evolution
Gone in 60 Seconds
Wanted
The Man with One Red Shoe
The Jerk
Whip It
Spanking the Monkey
Steel Magnolias
Horton Hears a Who
Honey
Brazil
Gorillas in the Mist
Before Sunset
After Dark
From Dusk til Dawn
Cloudy with a Chance of Meatballs
Harvey
Mr. Smith Goes to Washington
L.A. Confidential
Little Miss Sunshine
The Future
Howard the Duck
Howard's End
The Innkeeper
Revolutionary Road
""".splitlines()]


_default_node_modes = {
    'normal': {
        'fill': (0, 250, 0, 255),
        'pen': (0, 250, 0, 255),
        'line_width': 1.5,
    },
    'selected': {
        'fill': (255, 225, 0, 255),
        'pen': (200, 30, 50, 255),
        'line_width': 1.5,

    },
    'click': {
        'fill': (155, 200, 0, 255),
        'pen': (200, 200, 220, 255),
        'line_width': 1.5,
    },
    'hover': {
        'fill': (155, 200, 0, 255),
        'pen': (200, 80, 220, 255),
        'line_width': 1.5,
    },
}

_default_line_modes = {
    'normal': {
        'pen': (0, 255, 0, 255),
        'line_width': 1.5
    },
    'selected': {
        'pen': (120, 255, 255, 255),
        'line_width': 1.5
    },
    'hover': {
        'pen': (255, 255, 20, 255),
        'line_width': 1.5
    },
}


def rand_key():
    letters = (
        'ABCDEFGHIJKLMNOPQRSTUV'
        'abcdefghijklmnopqrstuv'
        '01234567890')
    rtn = ''
    for i in range(4):
        rtn += random.choice(letters)
    return rtn


_test_data = {
    'nodes': {
        'defg': {'name': 'Asterisk *',
                 'modes': _default_node_modes,
                 'tooltip': '*'},
        'bcde': {'name': 'Bang !',
                 'modes': _default_node_modes,
                 'tooltip': '!'},
        'abcd': {'name': 'Comma ,',
                 'modes': _default_node_modes,
                 'tooltip': ','},
    },
    'connections': {
        ('defg', 'bcde'): {'modes': _default_line_modes, 'weight': 1},
        ('abcd', 'defg'): {'modes': _default_line_modes, 'weight': 1},
    }
}


def _test():
    test_data = dict(_test_data)
    import random

    for i in range(30):
        key = rand_key()
        for _ in range(random.choice(range(1)) + 1):
            connection = random.choice(test_data['nodes'].keys())
            if connection == key:
                continue
            import copy
            node_mode = copy.deepcopy(_default_node_modes)
            edge_mode = copy.deepcopy(_default_line_modes)
            color = [random.random() * 55, random.random() * 255, random.random() * 50, 255]
            node_mode['normal']['fill'] = color
            node_mode['normal']['pen'] = color
            node_mode['selected']['pen'] = [155, 155, 155, 255]
            node_mode['selected']['fill'] = [155, 155, 155, 255]
            node_mode['hover']['pen'] = [255, 255, 255, 255]
            node_mode['hover']['fill'] = [255, 255, 255, 255]
            edge_mode['normal']['pen'] = color
            edge_mode['hover']['pen'] = [255, 255, 255, 255]
            edge_mode['selected']['pen'] = [155, 155, 155, 255]

            test_data['nodes'][key] = {
                'name': 'Comma ,',
                'modes': node_mode,
                'tooltip': ','}
            test_data['connections'][(key, connection)] = {
                'modes': edge_mode,
                'weight': 30,
            }

    app = QApplication(sys.argv)
    w = NodeViewer(node_data=test_data)
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.showFullScreen()
    w.raise_()
    sys.exit(app.exec_())


def test():
    from . import dag
    digraph = dag.DiGraph()
    n = []

    clus = ['foo', 'bar']
    clus = ['foo']

    import random
    taken = []

    def random_title():
        key = None
        while not key or key in taken:
            key = random.choice(_random_titles)
        taken.append(key)
        return key

    for i in range(900):
        color = [
            random.random() * 5,
            (random.random() * 150) + 55,
            random.random() * 10,
            255]
        k = dag.DagNode(random_title(), random.choice(clus), node_data={})
        k.style().set_attribute('fill_color', color, 'normal')
        k.style().set_attribute('pen_color', [0,color[1]*0.9,0,255], 'normal')
        k.style().set_attribute(
            'shape', random.choice(['star', 'rect', 'hexa', 'penta', 'round']), '_all_states_')
        k.style().set_attribute(
            'size',
            [(random.random() * 5) + 15, (random.random() * 5) + 15],
            '_all_states_')
        digraph.add_node(k)
        n.append(k)

    for node in n:
        for i in range(random.choice(range(1)) + 1):
            color = node.style().get_value('fill_color', 'normal')
            conn = random.choice(n)
            while node == conn:
                conn = random.choice(n)
            e = dag.DagEdge(node, conn, edge_data={})
            e.style().set_attribute('fill_color', color, 'normal')
            e.style().set_attribute('pen_color', color, 'normal')
            e.style().set_attribute('arrow_width', 5 + (random.random() * 8), 'normal')
            e.style().set_attribute('line_width', 2 + (random.random() * 3), 'normal')
            digraph.add_edge(e)

    b = dag.DagBox('sample_box', (100, 150),
                {'n': 0, 's': 1, 'w': 3, 'e': 2},
                random.choice(clus),
                box_data={})
    color = [200, 200, 150, 255]
    b.style().set_attribute('fill_color',  color, 'normal')
    b.style().set_attribute('pen_color',  color, 'normal')
    b.style().set_attribute('label_alignment', 'above', '_all_states_')
    digraph.add_box(b)
    for port in b.get_ports():
        port.set_label(random_title())

    for i in range(3):
        e = dag.DagEdge(b.get_port('w', i), random.choice(n), 100)
        e.style().set_attribute('line_style', 'dash', style._all_states)
        e.style().set_attribute('pen_color', [251, 250, 250, 255], 'normal')
        digraph.add_edge(e)

    for i in range(2):
        e = dag.DagEdge(random.choice(n), random.choice(b.get_ports()))
        e.style().set_attribute('line_style', 'dot', style._all_states)
        e.style().set_attribute('pen_color', [251, 250, 250, 255], 'normal')
        digraph.add_edge(e)

    for i in range(2):
        e = dag.DagEdge(b.get_port('e', 0), random.choice(n))
        e.style().set_attribute('line_style', 'dot', style._all_states)
        e.style().set_attribute('pen_color', [250, 250, 250, 255], 'normal')
        digraph.add_edge(e)
    digraph.process_dot()

    app = QApplication(sys.argv)
    w = NodeViewer()
    w.set_node_data(digraph)
    w.resize(450, 750)
    w.move(100, 100)
    w.setWindowTitle('Simple')
    w.showFullScreen()
    w.raise_()
    sys.exit(app.exec_())

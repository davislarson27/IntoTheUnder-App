import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import random

from world.world_creation.generate_world import Grid_Superstructure
from world.world_creation.world_generation_settings import World_Generation_Settings
from world.blocks.block_export import *


if __name__ == '__main__':
    # set values for testing
    count_of_tests = 40
    grid_width = 5000
    grid_height = 150
    ground_level = 50

    # test for blocks, None = all
    blocks_allowed_list = [Dirt, Grass, Gravel, Coal_Ore_Block, Iron_Ore_Block, Gold_Ore_Block, Emerald_Ore_Block, Diamond_Ore_Block, Mabelite_Ore_Block, Sulfur_Flakes_Block, Saltpeter, Recipe_Frame]

    # files for printing
    output_file_name = 'testing/results.txt'

    # initialize object to hold results
    foreground_block_counter = {}
    background_block_counter = {}

    foreground_worlds_with_block = {}
    background_worlds_with_block = {}

    foreground_min_depth = {}
    background_min_depth = {}

    foreground_max_depth = {}
    background_max_depth = {}

    foreground_tot_depth = {}
    background_tot_depth = {}

    for testNum in range(count_of_tests):
        print(f'running test {testNum+1} of {count_of_tests}')
        world_seed = int(random.random() * 100000000)
        world_generation_settings = World_Generation_Settings(0, 0, 0, grid_width, grid_height, 25)
        world_generation_settings.reset_ground_level(ground_level)
        grid_superstructure = Grid_Superstructure(None, world_generation_settings, None, world_seed=world_seed)
        grid_superstructure.generate_world()
        foreground_grid, background_grid = grid_superstructure.get_grids()

        fg_block_in_cur_iter = set()
        bg_block_in_cur_iter = set()

        for y in range(grid_height):
            for x in range(grid_width):
                # process foreground
                block = foreground_grid.get(x, y)
                if block is not None:
                    block = type(block)

                    if block not in foreground_block_counter:
                        foreground_block_counter[block] = 1
                    else:
                        foreground_block_counter[block] += 1
                    
                    fg_block_in_cur_iter.add(block)

                    if block not in foreground_tot_depth:
                        foreground_tot_depth[block] = y
                        foreground_max_depth[block] = y
                        foreground_min_depth[block] = y
                    else:
                        foreground_tot_depth[block] += y
                        foreground_max_depth[block] = max(foreground_max_depth[block], y)
                        foreground_min_depth[block] = min(foreground_min_depth[block], y)


                # process background
                block = background_grid.get(x, y)
                if block is not None:
                    block = type(block)

                    if block not in background_block_counter:
                        background_block_counter[block] = 1
                    else:
                        background_block_counter[block] += 1

                    bg_block_in_cur_iter.add(block)

                    if block not in background_tot_depth:
                        background_tot_depth[block] = y
                        background_max_depth[block] = y
                        background_min_depth[block] = y
                    else:
                        background_tot_depth[block] += y
                        background_max_depth[block] = max(background_max_depth[block], y)
                        background_min_depth[block] = min(background_min_depth[block], y)


        # now process which worlds have a certain block
        for block in fg_block_in_cur_iter:
            if block in foreground_worlds_with_block:
                foreground_worlds_with_block[block] += 1
            else:
                foreground_worlds_with_block[block] = 1

        for block in bg_block_in_cur_iter:
            if block in background_worlds_with_block:
                background_worlds_with_block[block] += 1
            else:
                background_worlds_with_block[block] = 1
        
    print('writing results...')

    # now write the results to the output file
    with open(output_file_name, 'w') as output:
        output.write(f'Results compiled from {count_of_tests} grids with a width of {grid_width}\n\n')

        output.write('Foreground Results\n\n')
        for block in foreground_block_counter:
            if blocks_allowed_list is None or block in blocks_allowed_list:
                avg_blocks_per_world = foreground_block_counter[block] / count_of_tests
                percent_worlds_with_block = foreground_worlds_with_block[block] / count_of_tests * 100
                avg_depth = foreground_tot_depth[block] / foreground_block_counter[block]

                output.write(f'{block.str_name}\n')
                output.write(f'   avg blocks: {avg_blocks_per_world:.1f}\n')
                output.write(f'   in world: {percent_worlds_with_block:.0f}%\n')
                output.write(f'   avg depth: {avg_depth:.0f} ({foreground_min_depth[block]}-{foreground_max_depth[block]})\n')

        output.write('\n\n')
        output.write('Background Results\n\n')
        for block in background_block_counter:
            if blocks_allowed_list is None or block in blocks_allowed_list:
                avg_blocks_per_world = background_block_counter[block] / count_of_tests
                percent_worlds_with_block = background_worlds_with_block[block] / count_of_tests * 100
                avg_depth = background_tot_depth[block] / background_block_counter[block]

                output.write(f'{block.str_name}\n')
                output.write(f'   avg blocks: {avg_blocks_per_world:.1f}\n')
                output.write(f'   in world: {percent_worlds_with_block:.0f}%\n')
                output.write(f'   avg depth: {avg_depth:.0f} ({background_min_depth[block]}-{background_max_depth[block]})\n')


        output.write('\n\n')
        output.write('Foreground Blocks Per Thousand\n\n')
        for block in foreground_block_counter:
            if blocks_allowed_list is None or block in blocks_allowed_list:
                avg_blocks_per_world = foreground_block_counter[block] / count_of_tests / grid_width * 1000

                output.write(f'{block.str_name}: {avg_blocks_per_world:.1f}\n')
    print('finished!')
    